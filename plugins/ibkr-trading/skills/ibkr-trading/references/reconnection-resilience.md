# Reconnection, Resilience, and Windows Production Deployment

## Daily Reset

TWS and IB Gateway perform a **daily reset** in the window **~23:45-00:45 ET** (North America). This is catastrophic for the socket API -- the connection ceases to exist (immediate error 502). Restart typically takes **1-5 minutes**, but intermittent interruptions can occur throughout the ~1 hour window. Native exchange orders continue to operate, but execution reports and simulated orders are delayed.

Since TWS 974+, **Auto Restart** (Configure -> Lock and Exit -> Auto Restart) allows restart without re-authentication, requiring manual login **only once a week** (Sunday, after Saturday night reset).

## Reconnection Pattern with ib_async

ib_async **has no built-in auto-reconnect**. The recommended pattern uses `disconnectedEvent`:

```python
import logging

log = logging.getLogger(__name__)

def on_disconnect():
    log.warning("Disconnected. Starting reconnect...")
    reconnect_with_backoff()

def reconnect_with_backoff():
    delays = [2, 5, 10, 20, 30, 30, 30]
    for attempt, delay in enumerate(delays):
        try:
            ib.connect("127.0.0.1", 4001, clientId=1, timeout=5)
            if ib.isConnected():
                resubscribe_all_data()
                verify_positions_and_orders()
                return
        except Exception:
            log.error(f"Attempt {attempt+1} failed. Retry in {delay}s")
            time.sleep(delay)  # OK here, outside the event loop

ib.disconnectedEvent += on_disconnect
```

### Post-Reconnection Mandatory Steps

After every reconnection:
1. Call `reqPositions()` to verify positions
2. Call `reqOpenOrders()` for open orders
3. Re-subscribe all market data (especially after error **1101** -- data lost)
4. Call `reqExecutions()` for fills that occurred during disconnection
5. Resume strategy logic only after state is verified

## IBC: Essential for Windows Production

**IBC** (https://github.com/IbcAlpha/IBC) is the de facto standard for TWS/Gateway automation:

- Automates login with username/password and handles 2FA prompts via IBKR Mobile
- Automatically handles TWS dialog boxes
- Includes **sample XML for Windows Task Scheduler** for daily auto-start
- Supports commands like `RECONNECTDATA` and `RECONNECTACCOUNT`
- Requires the offline/standalone version of TWS
- **Windows note**: use "Run only when user is logged on" in Task Scheduler for interactive access

## Critical Error Codes

### Connectivity (reqId = -1)

| Code | Meaning | Action |
|------|---------|--------|
| 1100 | Connectivity lost | Enter reconnect mode, halt trading |
| 1101 | Connectivity restored, **data lost** | Re-subscribe all market data |
| 1102 | Connectivity restored, data maintained | Resume normal operations |
| 2104/2106/2158 | Data farms connected (informational) | Log and ignore |
| 2103/2105 | Data farms disconnected | Wait for restoration, log |

### Handling Error Events

```python
def on_error(reqId, errorCode, errorString, contract):
    if errorCode in (1100,):
        log.critical(f"CONNECTIVITY LOST: {errorString}")
        halt_trading()
    elif errorCode == 1101:
        log.warning("Connectivity restored, DATA LOST -- resubscribing")
        resubscribe_all_data()
    elif errorCode == 1102:
        log.info("Connectivity restored, data maintained")
    elif errorCode in (2104, 2106, 2158):
        log.debug(f"Farm connected: {errorString}")
    elif errorCode in (2103, 2105):
        log.warning(f"Farm disconnected: {errorString}")
    elif errorCode == 201:
        log.error(f"ORDER REJECTED reqId={reqId}: {errorString}")
    else:
        log.warning(f"Error {errorCode} reqId={reqId}: {errorString}")

ib.errorEvent += on_error
```

## Heartbeat and Health Check

Use `reqCurrentTime()` as heartbeat, calling every 30-60 seconds. In ib_async, `ib.setTimeout()` sets a timeout for incoming messages and emits `timeoutEvent` if no data arrives for too long. Monitor last tick timestamps per instrument -- during market hours, if no update for >60 seconds on a liquid instrument, data may be stale.

```python
async def heartbeat_loop(ib):
    while ib.isConnected():
        try:
            server_time = await asyncio.wait_for(
                ib.reqCurrentTimeAsync(), timeout=10
            )
            log.debug(f"Heartbeat OK: server_time={server_time}")
        except asyncio.TimeoutError:
            log.error("Heartbeat timeout -- connection may be dead")
            on_disconnect()
            return
        await asyncio.sleep(30)
```

## Windows Production Deployment

### Firewall Rules

Windows Firewall can block TWS/Gateway's Java process. Create inbound rules for API ports (7496/7497/4001/4002). Only allow localhost connections:

```
netsh advfirewall firewall add rule name="IB Gateway API" dir=in action=allow protocol=TCP localport=4001,4002 remoteip=127.0.0.1
```

### Antivirus

Some AV solutions flag TWS as suspicious. Add the TWS/Gateway installation directory to exclusions.

### Memory

Increase Java heap to **4096 MB minimum** in Configure -> Settings -> Memory Allocation to prevent crashes with high data volumes. Monitor Python memory as well -- ib_async bar/ticker objects accumulate over time and must be trimmed.

### WinError 10038

Windows-specific socket error when the connection closes improperly. Handle in exception catching:

```python
except OSError as e:
    if e.winerror == 10038:  # Socket operation on non-socket
        log.warning("WinError 10038: connection already closed")
    else:
        raise
```

### Task Scheduler + IBC

The standard combination for automated Windows deployment:
1. Create a Task Scheduler task to run IBC startup script at system boot
2. Set "Run only when user is logged on" for interactive access
3. Configure restart on failure with appropriate delay
4. IBC handles Gateway login, 2FA, and daily restart

### Auto-logoff

Default at 23:45 local time -- configurable via Global Configuration -> Lock and Exit.

## Paper Trading Caveats

Paper trading uses **simulated execution** from top-of-book only. Key differences:

- Order types not supported: VWAP, Auction, RFQ, Pegged to Market
- Stops and complex orders are always simulated -- behavior may differ from production
- Penny trading for US Options not supported
- Simulator rejects residual of exchange-directed market orders that execute partially
- **Test in paper but never assume identical behavior to live**

## Community Resources and Reference Architectures

### GitHub Repositories

- **pysystemtrade** (https://github.com/pst-group/pysystemtrade): gold standard reference -- Rob Carver's fully automated futures trading system running 20 hours/day in production. Uses ib_insync, MongoDB, cron-job scheduling. Maintained by pst-group with Andy Geach since January 2026.
- **9600dev/mmr** (https://github.com/9600dev/mmr): LLM-native platform with ib_async + ZeroMQ + DuckDB, modern proposal-based order management
- **omdv/ibkr-trading** (https://github.com/omdv/ibkr-trading): reference for Docker + Kubernetes + Terraform deployment with ib_async
- **gnzsnz/ib-gateway-docker** (https://github.com/gnzsnz/ib-gateway-docker): best Docker image for IB Gateway with IBC, supports dual live+paper

### Guides and Tutorials

- AlgoTrading101 -- IB Python Native API: https://algotrading101.com/learn/interactive-brokers-python-api-native-guide/
- AlgoTrading101 -- ib_insync guide: https://algotrading101.com/learn/ib_insync-interactive-brokers-api-guide/
- Rob Carver's blog: https://qoppac.blogspot.com/2017/03/interactive-brokers-native-python-api.html (multi-part series, battle-tested)
- Book: "Algorithmic Trading with Interactive Brokers" by Matthew Scarpino
- YouTube -- Part Time Larry: complete beginner tutorials with ib_insync
- YouTube -- ML Algo Trader (https://youtube.com/@mlalgotrader): cited in ib_async README

### Active Communities

- Reddit r/algotrading (500k+ members): most active for IB + Python discussions
- Elite Trader IB Forum: https://www.elitetrader.com/et/forums/interactive-brokers.10/
- IBKR Campus Quant Blog: https://www.interactivebrokers.com/campus/ibkr-quant-news/
- Stack Overflow (tags: `interactive-brokers`, `ib-insync`): moderate activity, useful for specific problems
