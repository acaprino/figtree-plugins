# Event-Driven Market Data and Historical Data

## Subscription Types and Limits

### reqMktData -- Streaming Level 1 Quotes

Provides time-sampled Level 1 data (not every individual tick). Supports continuous streaming or single snapshots. Snapshots do not consume market data lines and cost **$0.01** per snapshot for US equity. Additional tick types specified via `genericTickList` (e.g., `'233'` for Time & Sales with VWAP).

```python
ticker = ib.reqMktData(contract, genericTickList='233', snapshot=False)
ib.pendingTickersEvent += on_tick

def on_tick(tickers):
    for t in tickers:
        print(f"{t.contract.symbol}: bid={t.bid} ask={t.ask} last={t.last} volume={t.volume}")
```

### reqRealTimeBars -- 5-Second Aggregated Bars

Produces **exclusively 5-second bars** -- the barSize parameter must be 5, no other value accepted. Critical advantage: after a network interruption, **missing bars are automatically backfilled** on reconnection. Disadvantage: the list grows indefinitely in memory -- must be trimmed periodically.

```python
bars = ib.reqRealTimeBars(contract, barSize=5, whatToShow='TRADES', useRTH=False)
bars.updateEvent += on_realtime_bar

def on_realtime_bar(bars, hasNewBar):
    if hasNewBar:
        bar = bars[-1]
        print(f"5s bar: O={bar.open} H={bar.high} L={bar.low} C={bar.close} V={bar.volume}")
    # Trim memory for long runs
    if len(bars) > 2000:
        del bars[:len(bars) - 1000]
```

### reqTickByTickData -- Individual Ticks

Provides every individual tick, but with a severe limitation: **max 3 simultaneous subscriptions** per connection. Available types: `'Last'`, `'AllLast'`, `'BidAsk'`, `'MidPoint'`.

```python
ticker = ib.reqTickByTickData(contract, tickType='AllLast')
```

### reqHistoricalData with keepUpToDate=True -- Live Tail

The most versatile approach for real-time bars at any standard timeframe (5 sec, 1 min, 5 min, 1 hour, etc.). The `endDateTime` must be an empty string. Updates arrive approximately every 5 seconds.

```python
bars = await ib.reqHistoricalDataAsync(
    contract, endDateTime='', durationStr='2 D',
    barSizeSetting='5 mins', whatToShow='TRADES',
    useRTH=False, keepUpToDate=True)
bars.updateEvent += on_bar_update
```

**Critical caveat**: the ib_insync documentation itself warns that "reqHistoricalData + keepUpToDate will leave the entire API inoperable after a network interruption." **reqRealTimeBars is more resilient** for automatic reconnection.

### Building on_new_candle

```python
def on_bar_update(bars, hasNewBar):
    if hasNewBar:
        completed_bar = bars[-2]  # Just-completed bar
        # Execute strategy logic here
    # Trim memory for long runs
    if len(bars) > 1000:
        del bars[:len(bars) - 500]
```

For non-standard timeframes (e.g., 7 minutes), aggregate from 5-second bars of `reqRealTimeBars` with a custom BarAggregator tracking the current period and emitting a callback on each aggregated bar close.

## Market Data Lines

Market data lines are shared between TWS and all API connections. Default: **100 lines**, expandable with Quote Booster Pack ($30/month per +100 lines, max 10 packs = 1,100 total) or based on account equity. Each streaming `reqMktData`, `reqRealTimeBars`, and `reqHistoricalData` with keepUpToDate consumes 1 line. Check current usage: **Ctrl+Alt+=** in TWS.

## Market Data Types

Call `ib.reqMarketDataType(1)` for live data (requires paid exchange subscriptions), `reqMarketDataType(3)` for delayed (free, 15-20 min delay). Forex and crypto **do not require subscriptions** for live data. Paper accounts can share market data from the associated live account.

## Historical Data

### Bar Sizes and Duration Limits

| Bar Size | Max Duration | Notes |
|----------|-------------|-------|
| 1 secs - 30 secs | 6 months | Tick-level precision, high request count |
| 1 min - 30 mins | 5-10+ years | Standard intraday analysis |
| 1 hour | 5-10+ years | Swing trading |
| 1 day - 1 month | Full history | End-of-day, weekly, monthly |

Each bar contains: Open, High, Low, Close, Volume, WAP (Weighted Average Price), BarCount.

### whatToShow Parameter

| whatToShow | Volume | Typical Use |
|-----------|--------|------------|
| **TRADES** | Yes | Stocks, futures -- real trade data, split-adjusted |
| **MIDPOINT** | No | **Forex** (TRADES unavailable), CFD |
| **BID/ASK** | No | Spread analysis, execution price estimation |
| **BID_ASK** | No | Average bid in Open, average ask in Close -- **counts as 2 requests** |
| **ADJUSTED_LAST** | Yes | Backtesting total return (split + dividend adjusted) |

- **Forex**: always use `MIDPOINT` -- no centralized trade tape exists
- **Stocks**: `TRADES` for standard data, `ADJUSTED_LAST` for accurate backtesting with dividends
- **Indices**: only `TRADES` available (no BID/ASK/MIDPOINT)

**Data quality caveat**: IB historical data is **NBBO-filtered** -- excludes odd lots, combo legs, block trades. Historical volume will be **lower** than unfiltered real-time volume. For futures, the daily bar close may be the **settlement price**, available even hours after close (Friday possibly Saturday).

### Extended Hours

Set `useRTH=0` to include pre-market (4:00-9:30 ET) and after-hours (16:00-20:00 ET). Extended hours data typically has much lower volume, wider spreads, and potential gaps.

## Pacing Violations

Pacing violations (error **162**) occur when:

- **Identical requests within 15 seconds** (same contract, same parameters)
- **6+ requests** for the same contract/exchange/tick-type **in 2 seconds**
- **More than 60 requests** in any **10-minute window**
- **BID_ASK requests count double** toward the 60 limit
- Max **50 simultaneous open historical requests**

### Best Practices to Avoid Pacing

- Space requests at least **10-15 seconds** apart
- Cache data locally (SQLite, Parquet)
- Use maximum duration per bar size to minimize request count
- Use `reqHeadTimeStamp()` to know the available start point before requesting

### Throttled Request Queue

```python
import asyncio

class HistoricalDataThrottle:
    def __init__(self, max_per_10min=50, min_interval=11):
        self.semaphore = asyncio.Semaphore(max_per_10min)
        self.min_interval = min_interval
        self.last_request = 0

    async def request(self, ib, contract, **kwargs):
        async with self.semaphore:
            now = asyncio.get_event_loop().time()
            wait = self.min_interval - (now - self.last_request)
            if wait > 0:
                await asyncio.sleep(wait)
            self.last_request = asyncio.get_event_loop().time()
            return await ib.reqHistoricalDataAsync(contract, **kwargs)
```

## Building a Robust OHLCV Feed

The hybrid approach is most resilient for production:

1. **Startup**: backfill from local database to last timestamp up to now
2. **Live**: subscribe to `reqRealTimeBars` (more robust than keepUpToDate for reconnection)
3. **Local aggregation**: aggregate 5-sec bars into the desired timeframe
4. **Periodic reconciliation**: compare with historical data to identify gaps
5. **Reconnection handling**: on error 1101/1102, request historical data for the disconnection period

## Data Error Codes

| Code | Meaning | Recovery |
|------|---------|----------|
| 162 | Pacing violation or HMDS error | Implement rate limiting with queue |
| 200 | Security definition not found | Verify contract specs |
| 354 | Not subscribed to market data | Subscribe or switch to delayed data |
| 321 | Bad tick type list | Check genericTickList parameter |
| 10197 | Using delayed data | Informational, subscribe for real-time |
