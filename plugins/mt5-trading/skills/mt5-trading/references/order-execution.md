# Order Execution and Management

## order_send() and MqlTradeRequest

`order_send()` accepts a dictionary with the fields of the `MqlTradeRequest` structure. Critical fields: `action` (operation type), `symbol`, `volume`, `type` (order type), `price`, `type_filling`, `deviation`, `magic`, `sl`, `tp`.

### Action Types

| Action | Constant | Use |
|--------|----------|-----|
| Market order | `TRADE_ACTION_DEAL` | Immediate execution |
| Pending order | `TRADE_ACTION_PENDING` | Place limit/stop |
| Modify SL/TP | `TRADE_ACTION_SLTP` | Change stops on existing position |
| Modify order | `TRADE_ACTION_MODIFY` | Change pending order parameters |
| Remove order | `TRADE_ACTION_REMOVE` | Cancel pending order |
| Close by | `TRADE_ACTION_CLOSE_BY` | Close against opposite position (hedging only) |

### Order Types

BUY, SELL, BUY_LIMIT, SELL_LIMIT, BUY_STOP, SELL_STOP, BUY_STOP_LIMIT, SELL_STOP_LIMIT, CLOSE_BY.

## Fill Modes -- The Most Common Production Error

**The most frequent production error is retcode 10030 (TRADE_RETCODE_INVALID_FILL).** Each symbol supports specific fill modes, verifiable via `symbol_info().filling_mode` (bit flag).

| Mode | Behavior | Typical Use |
|------|----------|-------------|
| **Fill or Kill (FOK)** | Full volume or nothing | Standard for Instant Execution |
| **Immediate or Cancel (IOC)** | Fill maximum available, cancel rest. Can give partial fills (retcode 10010) | Flexible execution |
| **Return** | Partial fill leaves residual as active order | **Prohibited in Market Execution** (most ECN/STP brokers) |
| **Book or Cancel (BOC)** | Passive orders only (limit/stop-limit), cancelled if would execute immediately | Maker-only strategies |

### Dynamic Fill Mode Detection

**Never hardcode fill modes.** They change between brokers and symbols.

```python
import MetaTrader5 as mt5

def get_filling_type(symbol):
    info = mt5.symbol_info(symbol)
    if info is None:
        return None
    filling = info.filling_mode
    if filling & 1:
        return mt5.ORDER_FILLING_FOK
    elif filling & 2:
        return mt5.ORDER_FILLING_IOC
    return mt5.ORDER_FILLING_RETURN
```

### Deviation (Slippage)

The `deviation` parameter specifies maximum acceptable slippage in **points** (not pips). **Only effective with Instant Execution** -- with Market Execution (ECN/STP) it is ignored. Recommended values: 10-20 points normally, 50+ during news.

## Hedging vs Netting

The mode is fixed at account creation (`account_info().margin_mode`): 0=netting, 2=exchange, 3=hedging.

**Most forex retail brokers use hedging** (replicates MT4 behavior).

| Aspect | Netting | Hedging |
|--------|---------|---------|
| Position model | Single net position per symbol | Multiple independent positions |
| BUY 1.0 + BUY 0.5 | One position of 1.5 lots at average price | Two separate positions |
| Close | Send opposite order | Must specify `position` field with ticket |
| Common error | N/A | Forgetting ticket creates new position instead of closing |

### Closing a Position in Hedging Mode

```python
def close_position(position):
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": position.symbol,
        "volume": position.volume,
        "type": mt5.ORDER_TYPE_SELL if position.type == 0 else mt5.ORDER_TYPE_BUY,
        "position": position.ticket,  # CRITICAL: must specify ticket in hedging
        "type_filling": get_filling_type(position.symbol),
        "magic": position.magic,
        "comment": "close",
    }
    return mt5.order_send(request)
```

## Complete Market Order Example

```python
def market_buy(symbol, volume, sl_points=None, tp_points=None, magic=12345):
    mt5.symbol_select(symbol, True)
    tick = mt5.symbol_info_tick(symbol)
    info = mt5.symbol_info(symbol)
    if tick is None or info is None:
        return None

    price = tick.ask
    point = info.point

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": round(price - sl_points * point, info.digits) if sl_points else 0.0,
        "tp": round(price + tp_points * point, info.digits) if tp_points else 0.0,
        "deviation": 20,
        "magic": magic,
        "comment": "python_bot",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": get_filling_type(symbol),
    }

    # Always check before sending
    check = mt5.order_check(request)
    if check is None or check.retcode != 0:
        print(f"Order check failed: {check}")
        return None

    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Order failed: retcode={result.retcode} comment={result.comment}")
    return result
```

## Return Codes

The result of `order_send()` contains `retcode`, `deal` (deal ticket), `order` (order ticket), `volume`, `price` (executed price), `bid`, `ask`, `comment`.

**Success check: `retcode == 10009` (TRADE_RETCODE_DONE).**

| Code | Constant | Meaning | Recovery |
|------|----------|---------|----------|
| 10004 | REQUOTE | Price changed | Re-fetch price and retry |
| 10009 | DONE | Success | Record fill |
| 10010 | DONE_PARTIAL | Partial fill (IOC) | Check filled volume |
| 10013 | INVALID | Invalid request | Check all fields |
| 10016 | INVALID_STOPS | SL/TP too close to price | Check `stops_level` |
| 10019 | NO_MONEY | Insufficient margin | Reduce volume or close positions |
| 10024 | TOO_MANY_REQUESTS | Rate limited | Exponential backoff, min 100-200ms |
| 10027 | CLIENT_DISABLES_AT | Autotrading disabled | Check terminal Ctrl+E |
| 10029 | FROZEN | Order in freeze zone | Cannot modify, wait |
| 10030 | INVALID_FILL | Wrong fill mode | Use dynamic fill mode detection |

## Pre-Trade Risk Check

**Always** use `order_check()` before `order_send()`. It validates fields, margin, fill mode, and volume **without sending to the server**. Returns `balance`, `equity`, `margin`, `margin_free`, `margin_level`, and `profit` post-operation.

Combine with:
- `order_calc_margin()` to calculate required margin
- `order_calc_profit()` to estimate P&L

## Magic Number

The `magic` is a 64-bit integer that persists in orders and positions, survives terminal restarts. **`magic=0` conventionally indicates manual trades** -- always use non-zero values for bots. Filter positions: `[p for p in positions if p.magic == MY_MAGIC]`. For multi-strategy setups, assign unique magic per strategy+symbol.

## Broker Differences: ECN vs Market Maker

| Aspect | ECN/STP | Market Maker |
|--------|---------|-------------|
| Execution mode | Market Execution | Instant Execution |
| Requotes | None | Possible (10004) |
| Deviation | Ignored | Respected |
| Slippage | Bidirectional | Typically only negative |
| stops_level | Often 0 (ideal for scalping) | Usually > 0 |

**Always query symbol properties at runtime**: `trade_exemode`, `trade_stops_level`, `trade_freeze_level`, `filling_mode`, `volume_min/max/step`. Never hardcode these values -- they change between brokers, between symbols, and over time.

## Best Practices

- Server-side SL/TP on every position -- non-negotiable safety net
- `order_check()` before every `order_send()`
- Dynamic fill mode detection per symbol, every time
- Magic number for every bot order (never 0)
- Specify position ticket when closing in hedging mode
- Handle all retcodes, especially 10030 (fill mode) and 10016 (stops level)
- Check `symbol_select()` before any trading or data operation
- Never hardcode broker-specific values (stops_level, filling_mode, etc.)
