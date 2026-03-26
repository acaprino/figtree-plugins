# MT5 Python API Architecture

## Overview

The `MetaTrader5` package on PyPI is developed and maintained by **MetaQuotes Ltd.** (MIT license). First release: March 2019, 61 releases to date. Version numbers correspond to MT5 platform build numbers. Current version: **5.0.5640**, supports Python 3.6-3.13.

Install: `pip install MetaTrader5`

The API communicates with the MT5 terminal via **Windows named pipes** (local IPC). Python and the MT5 terminal must run **on the same Windows machine**. Every API call is a synchronous request-response through the pipe: no callbacks, no push events, no socket connection. The underlying library is compiled in C for performance.

Official documentation: https://www.mql5.com/en/docs/python_metatrader5
Individual function docs: `https://www.mql5.com/en/docs/python_metatrader5/mt5{functionname}_py`
MetaEditor integration: https://www.metatrader5.com/en/metaeditor/help/development/python
Release notes: https://www.metatrader5.com/en/releasenotes

## The 32 Functions

The API exposes 32 functions across five functional areas:

**Connection**: `initialize()`, `login()`, `shutdown()`, `version()`, `last_error()`

**Account/Terminal info**: `account_info()`, `terminal_info()`

**Symbols**: `symbols_total()`, `symbols_get()`, `symbol_info()`, `symbol_info_tick()`, `symbol_select()`

**Market depth**: `market_book_add()`, `market_book_get()`, `market_book_release()`

**Historical data**: `copy_rates_from()`, `copy_rates_from_pos()`, `copy_rates_range()`, `copy_ticks_from()`, `copy_ticks_range()`

**Orders and positions**: `orders_total()`, `orders_get()`, `order_calc_margin()`, `order_calc_profit()`, `order_check()`, `order_send()`, `positions_total()`, `positions_get()`

**History**: `history_orders_total()`, `history_orders_get()`, `history_deals_total()`, `history_deals_get()`

## API Limitations

- **Windows-only**: named pipes IPC, no cross-platform support natively
- **No exceptions**: errors fail silently returning `None`. Must check every return value and call `last_error()`
- **No type hints, no docstrings, no context manager, no logging**
- **Single connection per process**: one Python process connects to one MT5 terminal
- **Not thread-safe**: the IPC pipe is single -- concurrent access causes race conditions, crashes, or corrupted data
- **No callbacks/streaming**: pure request-response, polling is the only approach
- **No Strategy Tester access**: backtesting is MQL5-only

## MQL5 EA vs Python API

MQL5 Expert Advisors run **inside** the terminal process with access to:
- Native event handlers: `OnTick()`, `OnTimer()`, `OnTrade()`, `OnTradeTransaction()`, `OnBookEvent()`, `OnChartEvent()`
- Strategy Tester with cloud optimization
- Chart objects, custom indicators, OpenCL acceleration

The Python API **has no access to any of these**. Python and MQL5 EAs can coexist: EAs run on charts while Python operates externally. The terminal offers "Disable automatic trading via external Python API" which blocks Python trading (retcode 10027) while keeping EAs active.

**Strategy Tester is exclusively for MQL5 programs.** Socket functions are blocked in the tester, making MQL5-to-Python communication impossible during backtest. Workaround: use Python backtesting frameworks (Backtrader, Backtesting.py) fed with historical data downloaded via API.

## Alternative Libraries

### aiomql (Recommended for async)

https://github.com/Ichinga-Samuel/aiomql (~109 stars, actively maintained)

The most mature async framework. Wraps every MT5 function with `asyncio.to_thread()`, adds automatic reconnection, a Bot orchestrator for multiple strategies on different instruments, session management (London/NY/Tokyo), integrated risk management, trailing stops, and CSV/JSON/SQLite recording. Remains polling-based internally but with clean async abstractions.

### MQL5-JSON-API (True streaming via ZeroMQ)

https://github.com/khramkov/MQL5-JSON-API

A complete ZeroMQ bridge: an MQL5 EA acts as server with dedicated ports for real-time tick streaming, candle streaming, and trade transaction events. Python connects via `zmq.SUB` and receives true push notifications. **This is the only architecture providing true event-driven on MT5**, the most similar conceptually to the IB TWS API. Requires installing the MQL5 EA and configuring ZeroMQ.

### mt5linux (Linux via Wine)

https://github.com/lucas-campagna/mt5linux (~116 stars)

Uses Wine + RPyC to run MT5 API from Linux. Classified as **inactive**. Updated fork: https://github.com/hpdeandrade/pymt5linux with Python 3.13 and Docker support.

### Others

- **pymt5adapter**: added context manager, exceptions, logging -- **deprecated**
- **pymt5** (DevCartel): for gateway broker use, not retail trading
- **metaapi-cloud-sdk**: WebSocket streaming, cross-platform, but **paid cloud service**

## Library Comparison

| Library | Streaming | Async | Cross-platform | Active | Best For |
|---------|-----------|-------|----------------|--------|----------|
| MetaTrader5 official | Polling | Sync | Windows only | Yes | Direct access, low overhead |
| aiomql | Async polling | asyncio | Windows only | Yes | **Best Python-pure framework** |
| MQL5-JSON-API (ZMQ) | True streaming | Yes | Any | Moderate | **True event-driven** |
| metaapi-cloud-sdk | WebSocket | Yes | Any | Yes | Cross-platform (paid) |

## Comparison with IBKR TWS API

The IB TWS API is **natively event-driven**: `EClient` for requests, `EWrapper` for callbacks (`tickPrice()`, `orderStatus()`, `execDetails()`). MT5 Python requires building the entire event system from scratch.

| Aspect | MT5 Python | IBKR TWS API |
|--------|-----------|--------------|
| Architecture | Synchronous polling | Event-driven callbacks |
| Rate limits | None documented (local IPC) | 50 msg/sec, pacing rules |
| Data cost | Included with account | Paid exchange subscriptions |
| Data source | Broker-dependent (varies) | Exchange-sourced (consistent) |
| Cross-platform | Windows only | Windows, Linux, macOS |
| Backtesting | External frameworks only | Not via API (external too) |
| Thread safety | Not thread-safe | Thread-based (EReader pattern) |
| Streaming | Polling only (or ZMQ bridge) | Native callbacks |
