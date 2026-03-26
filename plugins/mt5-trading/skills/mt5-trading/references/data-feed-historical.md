# Data Feed: Functions, Depth, and Data Quality

## The Three copy_rates Functions

### copy_rates_from_pos(symbol, timeframe, start_pos, count)

Selects by relative index (0 = current bar). Ideal for live trading: "give me the last 200 bars".

```python
rates = mt5.copy_rates_from_pos("EURUSD", mt5.TIMEFRAME_H1, 0, 200)
```

### copy_rates_from(symbol, timeframe, date_from, count)

Selects N bars starting from a date (going backward). Useful for fixed-size historical windows.

```python
from datetime import datetime
import pytz

utc = pytz.timezone("Etc/UTC")
rates = mt5.copy_rates_from("EURUSD", mt5.TIMEFRAME_D1, datetime(2024, 1, 1, tzinfo=utc), 365)
```

### copy_rates_range(symbol, timeframe, date_from, date_to)

Selects all bars in a calendar interval. Most natural for historical dataset downloads. The number of bars returned is variable.

```python
rates = mt5.copy_rates_range(
    "EURUSD", mt5.TIMEFRAME_M1,
    datetime(2024, 1, 1, tzinfo=utc),
    datetime(2024, 12, 31, tzinfo=utc)
)
```

All return **numpy structured arrays** with fields: `time` (Unix UTC), `open`, `high`, `low`, `close`, `tick_volume`, `spread`, `real_volume`.

### Timezone Caveat

**MT5 uses UTC internally.** Always create datetime objects in UTC:

```python
import pytz
utc = pytz.timezone("Etc/UTC")
dt = datetime(2024, 1, 1, tzinfo=utc)
```

Using naive datetime with local timezone is the most common cause of missing or incorrect data.

## Tick Data

`copy_ticks_from()` and `copy_ticks_range()` return arrays with: `time`, `bid`, `ask`, `last`, `volume`, `time_msc`, `flags`, `volume_real`.

### Tick Flags

- `COPY_TICKS_ALL`: all ticks
- `COPY_TICKS_INFO`: only bid/ask changes
- `COPY_TICKS_TRADE`: only last/volume changes

**Tick depth depends entirely on the broker**: from a few days to 1-2 years. EURUSD generates ~200,000+ ticks/day -- requesting months of data produces tens of millions of rows.

## Historical Depth

| Timeframe | Typical Depth |
|-----------|--------------|
| D1 | 20-30+ years |
| H1 | 10-15+ years |
| M1 | Weeks to ~2 years |
| Ticks | Days to 1-2 years (broker-dependent) |

**Set "Max bars in chart" to Unlimited** in MT5 Options -> Charts, otherwise results get truncated.

MT5 builds all intraday timeframes from stored M1 data. During weekends/holidays there are no bars -- no placeholders are inserted.

## Data Quality

### No Rate Limits

The local API **has no documented rate limits**. Calls complete in ~63us for small requests. The bottleneck is downloading from the broker server for data not cached locally.

### Broker-Dependent Quality

**Data quality varies dramatically between brokers:**

- ECN brokers provide more ticks and more accurate spreads
- Market makers may filter/aggregate ticks
- `tick_volume` varies between brokers for the same instrument
- `real_volume` is **always 0 for OTC forex** -- only available for exchange instruments
- The `spread` field records only the spread at bar close, not the average

### MT5 vs IBKR for Data

| Aspect | MT5 | IBKR |
|--------|-----|------|
| Rate limits | None (local IPC) | Strict pacing (15s, 60/10min) |
| Data cost | Included with account | Paid exchange subscriptions |
| Data source | Broker-dependent (varies) | Exchange-sourced (consistent) |
| Forex/CFD | More convenient | Requires subscriptions |
| Equity/futures (real volume) | Limited | Superior |

## Efficient Caching

### Bootstrap + Incremental Update

The recommended pattern:
1. Initial massive download on first run
2. On each subsequent run, determine last timestamp in cache
3. Request only new data since last timestamp

### Storage Format

**Parquet with Zstandard compression** is recommended by the community:
- Excellent compression (~5-10x)
- Preserves types
- Fast reads with pandas/pyarrow
- For tick data, partition by day/month

```python
import pandas as pd

# Download and save
rates = mt5.copy_rates_range("EURUSD", mt5.TIMEFRAME_M1, start, end)
df = pd.DataFrame(rates)
df['time'] = pd.to_datetime(df['time'], unit='s', utc=True)
df.to_parquet("eurusd_m1.parquet", compression="zstd")

# Load and update incrementally
existing = pd.read_parquet("eurusd_m1.parquet")
last_time = existing['time'].max()
new_rates = mt5.copy_rates_from("EURUSD", mt5.TIMEFRAME_M1, last_time, 10000)
if new_rates is not None and len(new_rates) > 0:
    new_df = pd.DataFrame(new_rates)
    new_df['time'] = pd.to_datetime(new_df['time'], unit='s', utc=True)
    combined = pd.concat([existing, new_df]).drop_duplicates(subset='time').sort_values('time')
    combined.to_parquet("eurusd_m1.parquet", compression="zstd")
```

## Market Depth (Level 2)

`market_book_add(symbol)` subscribes to depth updates. `market_book_get(symbol)` returns the current order book. `market_book_release(symbol)` unsubscribes. Note: even market depth requires polling -- there are no push notifications.

```python
mt5.market_book_add("EURUSD")
book = mt5.market_book_get("EURUSD")
if book:
    for entry in book:
        print(f"{'BUY' if entry.type == 1 else 'SELL'} {entry.volume} @ {entry.price}")
mt5.market_book_release("EURUSD")
```
