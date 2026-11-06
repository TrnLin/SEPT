---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [booking, data-model, fees]
repos: [rentxe]
---

# ADR — Extend a running rental by up to 30 days at a time

Context: With bookings capped at 30 days, a customer who wants the vehicle longer needs a way to keep it without returning it and booking again.
Decision: While a booking is `PICKED_UP`, from 7 days before its return date until the day before, the customer can ask for a new return date 1 to 30 days later. There is no limit on how many times (30 + 30 + 30, never 90 at once), but only one extension can wait at a time. The extra days must be free. The company approves or rejects; a waiting extension holds the extra days and expires like a booking request (24 hours, or at the start of the return day if sooner). On approval the same booking gets the new `endDate`, and its `totalPrice` grows by extra days × the booking's own daily rate and cover. Each request is kept in a `BookingExtension` row.
Why: The company keeps control of its vehicle, as with every booking. One booking means one pick-up, one return and one review, and reusing the request and expiry rules keeps the code small.
Rejected:
- Automatic extension when the days are free: the company loses control of a vehicle it has already handed over.
- Each extension as a new linked booking: the customer sees several bookings for one rental, reviews multiply, and the return-day rule would need an exception.
Trade-off: a new table and approve/reject endpoints for extensions, designed with the My bookings page and the company dashboard (no mockups yet).
Links: SRS §2.4, §2.8 · [api/vehicle.md](../api/vehicle.md) VEH-38, Q5 · [api/README.md](../api/README.md) BookingExtension, team decision 11
