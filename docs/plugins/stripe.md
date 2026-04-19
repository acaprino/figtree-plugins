# Stripe Plugin

> Integrate Stripe without reading 500 pages of docs. Covers payments, subscriptions, Connect marketplaces, billing, webhooks, and revenue optimization with ready-to-use patterns.

## Agents

### `stripe-integrator`

Complete Stripe API integrator covering payments, subscriptions, Connect marketplaces, billing, webhooks, and compliance.

| | |
|---|---|
| **Model** | `opus` |
| **Use for** | Payment processing, subscriptions, marketplaces, billing, webhooks, SCA/3DS compliance, fraud prevention, dispute handling |

**Invocation:**
```
Use the stripe-integrator agent to [integrate/audit/extend] [Stripe feature]
```

**Core capabilities:**
- **Payments** - Payment intents, checkout sessions, payment links
- **Subscriptions** - Recurring billing, metered usage, tiered pricing
- **Connect** - Marketplace payments, platform fees, seller onboarding
- **Billing** - Invoices, customer portal, tax calculation
- **Webhooks** - Signature-verified event handling, subscription lifecycle, idempotency
- **Security** - 3D Secure, SCA compliance, fraud prevention (Radar)
- **Disputes** - Chargeback handling, evidence submission

**Quick reference:**
| Task | Method |
|------|--------|
| Create customer | `stripe.Customer.create()` |
| Checkout session | `stripe.checkout.Session.create()` |
| Subscription | `stripe.Subscription.create()` |
| Payment link | `stripe.PaymentLink.create()` |
| Report usage | `stripe.SubscriptionItem.create_usage_record()` |
| Connect account | `stripe.Account.create(type="express")` |

**Prerequisites:**
```bash
export STRIPE_SECRET_KEY="sk_test_..."
export STRIPE_WEBHOOK_SECRET="whsec_..."
pip install stripe
```

---

### `revenue-optimizer`

Monetization expert. Analyzes your codebase to discover features, calculate service costs, model usage patterns, and create data-driven pricing strategies with revenue projections.

| | |
|---|---|
| **Model** | `opus` |
| **Use for** | Feature cost analysis, pricing strategy, usage modeling, revenue projections, tier design |

**Invocation:**
```
Use the revenue-optimizer agent to [analyze/design/project] [pricing|tiers|revenue]
```

**5-Phase Workflow:**
1. **Discover** - Scan codebase for features, services, and integrations
2. **Cost Analysis** - Calculate per-user and per-feature costs
3. **Design** - Create pricing tiers based on value + cost data
4. **Implement** - Build payment integration and checkout flows
5. **Optimize** - Add conversion optimization and revenue tracking

**Key Metrics Calculated:**
| Metric | Formula |
|--------|---------|
| ARPU | (Free x $0 + Pro x $X + Biz x $Y) / Total Users |
| LTV | (ARPU x Margin) / Monthly Churn |
| Break-even | Fixed Costs / (ARPU - Variable Cost) |
| Optimal Price | (Cost Floor x 0.3) + (Value Ceiling x 0.7) |

---

## Skills

### `stripe`

Stripe knowledge base -- API patterns, checkout optimization, subscription lifecycle, pricing strategies, webhook reliability, Firebase integration, cost analysis, revenue modeling. Loaded by `stripe-integrator` and `revenue-optimizer`; also usable standalone when you need patterns without agent invocation.

| | |
|---|---|
| **Invoke** | Skill reference |
| **Trigger** | Working with Stripe API (Payment Intents, Customers, Subscriptions, Checkout Sessions, Connect, webhooks, tax, usage-based billing), pricing strategy, or revenue modeling |

**References** (under `skills/stripe/references/`):
| File | Content |
|------|---------|
| `stripe.md` | Core concepts, current API version notes, pin patterns |
| `api-cheatsheet.md` | Quick API reference |
| `stripe-patterns.md` | Metered billing, Connect, tax, 3DS, Radar, disputes, idempotency |
| `checkout-optimization.md` | Conversion optimization patterns |
| `subscription-patterns.md` | Subscription lifecycle + state reconciliation |
| `pricing-patterns.md` | Tier design, pricing strategy |
| `cost-analysis.md` | Unit economics |
| `usage-revenue-modeling.md` | Usage-based revenue models |
| `firebase-integration.md` | Firebase + Firestore integration |

**Scripts** (`skills/stripe/scripts/`, reference via `${CLAUDE_PLUGIN_ROOT}/skills/stripe/scripts/`):
- `setup_products.py` -- bootstrap Products and Prices
- `webhook_handler.py` -- signature-verified receiver with idempotency
- `sync_subscriptions.py` -- reconcile local DB vs Stripe subscription state
- `stripe_utils.py` -- shared utilities

**Key section:** webhook reliability checklist (signature verification, raw body preservation, idempotency via `event.id`, 10-second 2xx response, replay testing).

---

**Related:** [python-development](python-development.md) (Python implementation patterns) | [business](business.md) (legal and compliance for payment flows)
