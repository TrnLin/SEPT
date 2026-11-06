---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [booking, search, vehicle]
repos: [rentxe]
---

# ADR — A booking is at most 30 days and starts at most 12 months ahead

Context: Nothing limited how long a rental could be or how far ahead it could start. One request could hold a vehicle for years, the calendar had no end, and a mistyped year (2062) was accepted.
Decision: A booking is 1 to 30 days long, and its pick-up date is at most 365 days after today (in the pick-up place's time zone). Search, compare, the quote and the booking request return `400` otherwise: "A rental can be at most 30 days" or "Pick-up can be at most 12 months ahead". The date pickers stop at these limits. The limits are the same for every company. Longer rentals use extensions ([extend-rental-by-30-days](extend-rental-by-30-days.md)).
Why: 30 days covers almost every rental and 12 months matches the calendar mockup. Two checks in the shared date validator stop one request from holding a vehicle for months and catch typos.
Rejected:
- No limits: the problems above.
- Only a 12-month horizon with any length: one request could still hold a vehicle for months.
Trade-off: a customer who needs more than 30 days books 30 and extends.
Links: SRS §2.3, §2.4, §2.8 · [api/vehicle.md](../api/vehicle.md) VEH-37, Q5 · [api/search.md](../api/search.md) SR-4 · [api/README.md](../api/README.md) team decision 11
