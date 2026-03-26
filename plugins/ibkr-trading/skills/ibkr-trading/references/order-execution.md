# Order Execution and Management

## Order Types

The fundamental principle: **any order placeable from TWS can be placed via API**. This includes:

| Type | API Code | Use Case |
|------|----------|----------|
| Market | `MKT` | Immediate fill, accepts slippage |
| Limit | `LMT` | Price control, may not fill |
| Stop | `STP` | Trigger on price breach |
| Stop-Limit | `STP LMT` | Stop with price protection |
| Trailing Stop | `TRAIL` | Dynamic trailing stop |
| MOC | `MOC` | Market on close |
| LOC | `LOC` | Limit on close |
| Market-to-Limit | `MTL` | Market that converts to limit after partial fill |
| Midprice | `MIDPRICE` | Pegged to midpoint |
| Relative/Pegged | `REL` | Pegged to NBBO |

IB algos are also available: **Adaptive** (priority: Urgent/Normal/Patient), TWAP, VWAP, ArrivalPx, DarkIce, Accumulate/Distribute, PctVol.

## Bracket Orders

Bracket orders (parent + take-profit + stop-loss) use parent-child order linking. The key pattern: set `transmit=False` on parent and first child, `transmit=True` only on the last child to send everything together. Each order requires a unique incremental `orderId`.

```python
from ib_async import *

def create_bracket_order(ib, contract, action, qty, entry_price, tp_price, sl_price):
    parent = LimitOrder(action, qty, entry_price)
    parent.orderId = ib.client.getReqId()
    parent.transmit = False

    # Take profit
    tp_action = 'SELL' if action == 'BUY' else 'BUY'
    take_profit = LimitOrder(tp_action, qty, tp_price)
    take_profit.orderId = ib.client.getReqId()
    take_profit.parentId = parent.orderId
    take_profit.transmit = False

    # Stop loss
    stop_loss = StopOrder(tp_action, qty, sl_price)
    stop_loss.orderId = ib.client.getReqId()
    stop_loss.parentId = parent.orderId
    stop_loss.transmit = True  # This triggers the entire bracket

    for order in [parent, take_profit, stop_loss]:
        ib.placeOrder(contract, order)

    return parent.orderId
```

## Order Lifecycle States

| Status | Meaning | Action |
|--------|---------|--------|
| ApiPending | Sent from API, not yet to TWS | Wait |
| PendingSubmit | Sent to IB, awaiting acknowledgment | Wait |
| PreSubmitted | Accepted by IB, held (e.g., stop order waiting for trigger) | Monitor |
| Submitted | Live in the market | Monitor |
| Filled | Fully executed | Record fill, update position |
| Cancelled | Cancelled by user or system | Check reason |
| Inactive | Order rejected, expired, or invalid | Check error code, investigate |

## Monitoring: Always Use execDetails

**Critical caveat**: `orderStatus` is **not guaranteed for every state change**. For market orders that fill instantly, you may never receive the orderStatus callback. **Always monitor `execDetails` as the authoritative source of fills.** `orderStatus` messages can be duplicated (echoed from TWS, IB server, exchange) -- filter duplicates in code.

```python
def on_exec_details(trade, fill):
    log.info(
        f"FILL: {fill.contract.symbol} {fill.execution.side} "
        f"qty={fill.execution.shares} price={fill.execution.avgPrice} "
        f"time={fill.execution.time} orderId={fill.execution.orderId}"
    )

ib.execDetailsEvent += on_exec_details
```

## Order ID Management

- `nextValidId` is sent immediately on connection
- IDs must be unique positive integers, always greater than the last used
- For multi-client setups, the ID must exceed all open order IDs
- Error **103** ("Duplicate order ID") is among the most frequent in production
- Use `ib.client.getReqId()` in ib_async for auto-increment

## Race Conditions

### Cancel-Fill Race

Between sending `cancelOrder()` and receiving confirmation, a fill can occur. **Never assume a cancel succeeded until you receive confirmation.** The sequence can be: cancelOrder() -> execDetails (fill) -> orderStatus(Cancelled for the residual).

```python
async def safe_cancel(ib, trade):
    """Cancel with fill-race awareness."""
    ib.cancelOrder(trade.order)
    # Wait for either cancellation or fill
    while trade.orderStatus.status not in ('Cancelled', 'Filled'):
        await asyncio.sleep(0.1)
    if trade.orderStatus.status == 'Filled':
        log.warning(f"Order {trade.order.orderId} filled during cancel attempt")
    return trade.orderStatus.status
```

### Partial Fills

Track cumulative filled quantity. Adjust bracket child quantities on partial fills if needed. The `trade.fills` list contains all individual fills for an order.

### Order Modification

`placeOrder()` with the same orderId = modify. Cannot modify already-filled portions. Cancellation may fail if the order is being filled simultaneously.

## Order Efficiency Ratio

IB tracks the ratio between submissions+modifications+cancellations and actual executions. Must stay **<= 20:1** -- exceeding it generates warnings and potential restrictions. Avoid rapid-fire order modifications.

## Message Rate Limit

**50 messages/second** toward IB. Exceeding this limit causes disconnection (error 100). Enable `SetConnectOptions("+PACEAPI")` to make TWS throttle instead of disconnect:

```python
ib.client.setConnectOptions('+PACEAPI')
```

## Position Reconciliation

Run on startup and periodically to detect state drift:

```python
async def reconcile_positions(ib, expected_positions):
    actual = await ib.reqPositionsAsync()
    for pos in actual:
        key = (pos.contract.symbol, pos.contract.secType)
        expected = expected_positions.get(key, 0)
        if pos.position != expected:
            log.error(
                f"POSITION MISMATCH: {key} expected={expected} actual={pos.position}"
            )
    # Also check for fills during disconnection
    fills = await ib.reqExecutionsAsync()
    for fill in fills:
        log.info(f"Reconciled fill: {fill.execution.orderId} {fill.execution.shares}@{fill.execution.avgPrice}")
```

## Order Error Codes

| Code | Meaning | Recovery |
|------|---------|----------|
| 103 | Duplicate order ID | Increment orderId and retry |
| 104 | Cannot modify filled order | Ignore modification |
| 110 | Price exceeds exchange limits | Adjust price |
| 161 | Cancel attempted on non-pending order | Already filled/cancelled |
| 200 | No security definition found | Verify contract specs |
| 201 | Order rejected | **Never retry automatically**, investigate reason |
| 202 | Order cancelled | Check reason (often price check failure) |
| 399 | Order message warning | Log and monitor |

## Best Practices

- Always use bracket orders for risk management
- Never submit parent with `transmit=True` before children are ready
- Log every order state transition
- Monitor `execDetails`, not just `orderStatus`
- Implement position reconciliation on startup and periodically
- Design assuming every cancel can fail (cancel-fill race)
- Keep order efficiency ratio well below 20:1
- Enable PACEAPI to avoid hard disconnects from message flooding
- Use paper trading for all development (but do not assume identical behavior to live)
