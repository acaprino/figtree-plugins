# TWS API Architecture and ib_async

## TWS API Overview

The TWS API is a proprietary TCP socket protocol (migrated to Protocol Buffers since version 10.40) connecting Python code to TWS or IB Gateway, which relay to IBKR servers. Current version: **10.44** (February 2026). Minimum supported TWS/Gateway: **10.30** (older versions blocked since March 2025). Python support: >=3.11.

Official documentation (migrated to IBKR Campus, old GitHub Pages docs are deprecated):

- API Home: https://www.interactivebrokers.com/campus/ibkr-api-page/ibkr-api-home/
- TWS API Docs: https://www.interactivebrokers.com/campus/ibkr-api-page/twsapi-doc/
- API Reference: https://www.interactivebrokers.com/campus/ibkr-api-page/twsapi-ref/
- Changelog: https://www.interactivebrokers.com/campus/ibkr-api-page/tws-api-changelog-2/
- 2026 Release Notes: https://ibkrguides.com/releasenotes/prod-2026.htm

## IB Gateway vs TWS

From the API perspective, TWS and IB Gateway are identical -- both are local TCP socket servers. The difference is operational.

| Aspect | TWS | IB Gateway |
|--------|-----|------------|
| Resources | ~40% more (full GUI) | **~40% less RAM/CPU** |
| API enabled by default | No, must enable manually | **Yes, ready to use** |
| Default ports (live/paper) | 7496 / 7497 | 4001 / 4002 |
| Auto-update | Available (online + offline) | Offline version only |
| GUI | Full (charts, order book) | Minimal (connection status) |

**IB Gateway is recommended for production** due to lower resource usage and smaller attack surface. Both support up to **32 simultaneous connections** with unique clientIds. Both require manual login (no truly headless mode for IB security reasons), but tools like **IBC** automate this.

**Critical**: use the **offline/standalone** version in production, never the auto-updating version -- unexpected updates break automations.

## Client Portal / Web API

IBKR is unifying web APIs into a single "IBKR Web API" (Client Portal + Digital Account Management + Flex Web Service) with OAuth 2.0. Docs: https://www.interactivebrokers.com/campus/ibkr-api-page/webapi-doc/

**Do not use the Web API for active algotrading.** Global limit: **10 requests/second** per session. Exceeding it puts the IP in penalty box for 10-15 minutes. Useful for account management, reporting, and portfolio monitoring in cloud contexts with OAuth. For low-latency trading, complex orders, and real-time streaming, the TWS API socket is the only serious choice.

## ib_async: The Current Standard

### History

**ib_insync** (by Ewald de Wit) was **archived March 14, 2024** after the author's unexpected passing. With ~3,200 stars and 860+ forks, it remains the largest knowledge base but **receives no updates**. Last PyPI version: 0.9.86.

The actively maintained successor is **ib_async** from the **ib-api-reloaded** organization:

- Repository: https://github.com/ib-api-reloaded/ib_async
- Documentation: https://ib-api-reloaded.github.io/ib_async/
- PyPI: `pip install ib_async` (current version: **2.1.0**)
- Last commit: January 2026, Python >=3.10
- Migration: nearly drop-in -- change `from ib_insync import *` to `from ib_async import *`

ib_async implements the IBKR binary protocol internally, **without depending on ibapi**. It provides an asyncio-native model with events (`pendingTickersEvent`, `barUpdateEvent`, `trade.fillEvent`), Jupyter support via `util.startLoop()`, and helpers like `qualifyContracts()` with automatic pandas DataFrame conversion.

### When to Use Official ibapi Instead

The official `ibapi` package uses a callback EWrapper/EClient pattern with explicit threading. **Not available updated on PyPI** -- the PyPI version (9.81.1) is from 2020 and severely outdated. Must be installed from the TWS API download: https://www.interactivebrokers.com/en/trading/ib-api.php

Prefer ibapi when: you need immediate access to just-released features, institutional contexts requiring only official libraries, or systems needing total threading control for sub-millisecond latency. For all other cases, **ib_async is superior in productivity and robustness**.

## Connection Setup

### Basic Connection Pattern

```python
from ib_async import *

async def main():
    ib = IB()
    await ib.connectAsync('127.0.0.1', 4001, clientId=1)

    contract = Stock('AAPL', 'SMART', 'USD')
    await ib.qualifyContractsAsync(contract)

    # Use the qualified contract for data/orders
    print(f"Qualified: {contract.conId}")

    ib.disconnect()

asyncio.run(main())
```

### Event Loop Approaches

Three approaches for the event loop:
- **Synchronous** (`ib.run()`): simplest for standalone bots
- **Fully async** (`asyncio.run()` with `*Async` methods): maximum control
- **Jupyter** (`util.startLoop()`): uses nest_asyncio for notebooks

**Fundamental rule**: never use `time.sleep()` -- it blocks the entire event loop and halts all message processing. Always use `ib.sleep(seconds)` or `asyncio.sleep()`, which yield control. For CPU-intensive work in callbacks, use `loop.run_in_executor()`.

### Threading vs asyncio

**asyncio (ib_async) is generally more robust** for production than threading (native ibapi) because it avoids thread synchronization issues, has cleaner error handling, and keeps state automatically synchronized. Key rule: never block the event loop for too long. When integrating with non-async frameworks (Flask, Django), run IBKR work in a **dedicated thread with its own asyncio loop** and communicate via queues.

## clientId Strategy

- `clientId=0` is special: merges with manual TWS trading, receiving visibility into manual orders
- For production bots, use dedicated IDs per function (e.g., 1=data, 2=orders, 3=monitoring)
- The **Master Client ID** (configurable in TWS) receives updates on all open orders from all clients
- Error **326** indicates clientId already in use
- Max 32 simultaneous connections

## Related Libraries

- **IBC** (https://github.com/IbcAlpha/IBC): login automation for TWS/Gateway, 2FA handling, auto-restart. **Essential for production.**
- **ibeam** (https://github.com/Voyz/ibeam): login automation for **Client Portal Web API** only (not TWS API). Useful only for REST API in Docker.
- **NautilusTrader** (https://github.com/nautechsystems/nautilus_trader): professional platform with IB adapter, backtesting + live in one framework.
- **Backtrader**: built-in IB support, good for prototyping, but development has slowed.
- **gnzsnz/ib-gateway-docker** (https://github.com/gnzsnz/ib-gateway-docker): Docker image with IB Gateway + IBC, supports simultaneous live+paper.
