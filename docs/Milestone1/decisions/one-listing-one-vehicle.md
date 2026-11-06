---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [search, vehicle, booking, data-model]
repos: [rentxe]
---

# ADR — One listing is one physical vehicle

Context: The search and vehicle mockups show "Only 2 left", but the README's Vehicle has one plate and one odometer, so the number had nothing to count. search.md assumed a `Vehicle.units` field to make it work.
Decision: One Vehicle is one physical vehicle. There is no `units` field. A company with three identical cars lists three vehicles. Availability for the searched dates is `AVAILABLE` or `BOOKED`; `FEW_LEFT` and `unitsLeft` are dropped, and so is the "Only N left" label on both pages.
Why: The model already treats each vehicle as one plate and one odometer, which pick-up, return and reviews depend on. Units would need per-day counting in search, the vehicle calendar and the booking clash check, for a label the brief doesn't ask for.
Rejected:
- `Vehicle.units`, with a booking taking one unit: a calendar day is only "booked" when every unit is taken, and pick-up and return would have to say which physical car was handed over.
Trade-off: a company with many identical vehicles adds each one separately, and they appear as separate rows in search. A "duplicate listing" button on the company dashboard can ease that later.
Links: SRS §2.2, §2.3 · [api/search.md](../api/search.md) SR-8, Q1 · [api/vehicle.md](../api/vehicle.md) Q12 · [api/README.md](../api/README.md) team decision 4
