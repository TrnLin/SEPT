---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [auth, ui, security, booking]
repos: [rentxe]
---

# ADR — Return customers to the page they came from after log in (`?next=`)

Context: A logged-out customer who clicks "Request to book" on a vehicle page has to log in first. Without a way back, they land on Search or My bookings (LOGIN-28) and must find the vehicle and pick their dates again, at the moment they were about to book.
Decision: Pages that send a logged-out user to log in pass the page they were on as `next`, for example `/login?next=/vehicles/68?start=2026-12-11&end=2026-12-14` (URL-encoded). After log in or sign-up, a customer goes to `next` instead of the LOGIN-28 page. Companies and admins ignore it. `next` is used only if it is a path on our own site (one leading `/`, no scheme or host, not the login page); anything else is ignored without an error. Returning never sends the booking by itself.
Why: Keeps the customer's vehicle and dates at the point they are most likely to book. The work is small: login links add `next`, and the login page checks and follows it.
Rejected:
- No return: simplest, but the customer loses their place right before booking.
- Accept any URL in `next`: allows an open redirect, where a crafted link logs a user in and then forwards them to a fake site.
Links: SRS §2.1, §3.2 · [api/login.md](../api/login.md) Q7, LOGIN-28, LOGIN-29 · [api/vehicle.md](../api/vehicle.md) `POST /api/v1/bookings` `401`
