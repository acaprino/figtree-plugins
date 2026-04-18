---
name: stripe
description: >
  Stripe payments knowledge base -- API patterns, checkout optimization, subscription lifecycle, pricing strategies, webhook reliability, Firebase integration, cost analysis, and revenue modeling. Loaded by stripe-integrator and revenue-optimizer agents; also consumable directly when the user asks for Stripe-specific patterns without needing an agent.
  TRIGGER WHEN: working with Stripe API (Payment Intents, Customers, Subscriptions, Checkout Sessions, Connect, webhooks, tax, usage-based billing), pricing strategy, or revenue modeling.
  DO NOT TRIGGER WHEN: payment work is non-Stripe (PayPal, Square, crypto) or the task is generic e-commerce unrelated to payments.
---

# Stripe Knowledge Base

Unified reference for Stripe integrations. Content is split across `references/` (topic-specific patterns) and `scripts/` (ready-to-run helpers).

## When to load which reference

- **Any Stripe API work** -> start with `references/api-cheatsheet.md` and `references/stripe.md`
- **Subscription lifecycle / billing** -> `references/subscription-patterns.md`, `references/usage-revenue-modeling.md`
- **Checkout conversion optimization** -> `references/checkout-optimization.md`
- **Pricing strategy and tier design** -> `references/pricing-patterns.md`
- **Firebase + Stripe integration** -> `references/firebase-integration.md`
- **Stripe-idiomatic patterns (reusable code)** -> `references/stripe-patterns.md`
- **Cost analysis / unit economics** -> `references/cost-analysis.md`

## Scripts

Ready-to-run Python helpers (adapt to your project; require `STRIPE_SECRET_KEY` env var):

- `scripts/setup_products.py` -- bootstrap Products and Prices for a new project
- `scripts/stripe_utils.py` -- shared utility functions used by the other scripts
- `scripts/sync_subscriptions.py` -- reconcile local DB vs Stripe subscription state
- `scripts/webhook_handler.py` -- signature-verified webhook receiver template with idempotency

All scripts live at `${CLAUDE_PLUGIN_ROOT}/skills/stripe/scripts/<name>.py`. Agents should reference them by that path.

## API version notes

Stripe rolls a new API version every few months. Pin an explicit version in all server-side code:

```python
import stripe
stripe.api_version = "2025-09-30.preview"  # or the latest dated version appropriate for your account
```

Client-side SDKs (stripe-node, stripe-python) now support `apiVersion` as a constructor option. Prefer setting it per-request rather than trusting the account default.

As of April 2026, the account default version for most Stripe accounts created in 2025+ is in the `2025-xx-xx` family. Dashboard -> Developers -> API version shows your current default.

## Webhook reliability checklist

- Verify signature with `stripe.Webhook.construct_event` on every event
- Use the raw body, not re-serialized JSON
- Idempotency: deduplicate by `event.id` (Stripe retries within a 3-day window)
- Always respond `2xx` within 10 seconds; defer heavy work to a queue
- Replay past events via `stripe events resend` during development
- Test signature failures -- attackers spoof webhooks

See `references/stripe-patterns.md` for the full handler template and `scripts/webhook_handler.py` for a working implementation.

## Common pitfalls

- Using `subscription.current_period_end` at top level -- it moved to `subscription.items.data[0].current_period_end` in newer API versions; verify against your pinned version
- Caching `customer.default_source` -- deprecated in favor of `invoice_settings.default_payment_method`
- Treating `price.id` as the product identifier -- `price.id` changes on any price update; use `product.id` for stable references
- Forgetting `automatic_payment_methods: { enabled: true }` on Payment Intents -- customers get a default payment-method list that often excludes wallets and BNPL

## Integration

- Pricing, tier design, revenue projections -> `revenue-optimizer` agent (same plugin)
- API implementation, webhooks, Connect, subscriptions -> `stripe-integrator` agent (same plugin)
- GDPR / PCI posture around payment data -> `business:privacy-doc-generator`
- Cross-platform token/auth handling in a payment flow -> `platform-engineering:platform-reviewer`
