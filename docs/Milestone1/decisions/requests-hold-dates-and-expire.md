---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [booking, search, vehicle, data-model]
repos: [rentxe]
---

# ADR — Booking requests hold their dates and expire after 24 hours

Context: A `REQUESTED` booking blocked its dates with no time limit, so a company that never answered could hold a vehicle for good and leave the customer waiting.
Decision: `REQUESTED`, `APPROVED` and `PICKED_UP` bookings block their dates. A request the company hasn't answered by its `expiresAt` becomes `EXPIRED` and frees its dates. `expiresAt` is 24 hours after the request is sent, or 00:00 on the pick-up day in the pick-up place's time zone if that is sooner. A scheduled job marks expired requests every 15 minutes, and every availability check already skips requests past `expiresAt`. The company can't approve after `expiresAt`. The customer sees "The company didn't answer in time".
Why: First come, first served keeps search honest: "Free" means the customer can actually book, and an approval can never clash. The deadline stops a slow company from holding a vehicle, and a separate `EXPIRED` status doesn't tell the customer they were rejected.
Rejected:
- Only `APPROVED` blocks, and approving one request rejects the overlapping ones: search shows "Free" while requests wait, customers get rejected after waiting, and approval needs more logic.
- Requests block and never expire: one silent company blocks its vehicles for good.
Trade-off: one more status, one stored timestamp and a scheduled job. Companies must answer within a day; the company dashboard should show the time left (later, with its mockup).
Links: SRS §2.4, §2.8 · [api/vehicle.md](../api/vehicle.md) VEH-6, VEH-21, VEH-36, Q1, Q2 · [api/search.md](../api/search.md) SR-6, Q2 · [api/README.md](../api/README.md) Booking, team decision 1
