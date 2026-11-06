---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [auth, ui, booking]
repos: [rentxe]
---

# ADR — Customers land on Search unless they have an active booking

Context: The login mockup sent customers to My bookings after both log in and sign up. A new customer has no bookings, so their first page was empty, and so was the page for a returning customer whose rentals were all finished.
Decision: After sign-up, a customer goes to Search. After log in, the page asks `GET /api/v1/bookings/summary`: with at least one active booking (`REQUESTED`, `APPROVED` or `PICKED_UP`) the customer goes to My bookings, otherwise to Search. If that call fails, Search. Companies still go to their dashboard and admins to the admin area.
Why: Someone with nothing in progress wants to find a vehicle next; someone with a request or a rental in progress usually logs in to check on it. The summary endpoint already exists for the nav count, so this needs no new API, only one call before the redirect.
Rejected:
- My bookings for everyone (the mockup): an empty page on a customer's first visit.
- Search for everyone: returning customers checking a request would need an extra click.
- Count every booking, including returned and cancelled ones: a customer with only past rentals would land on a page with nothing to act on.
Links: SRS §2.1 · [api/login.md](../api/login.md) Q3, LOGIN-13, LOGIN-28 · [api/search.md](../api/search.md) `GET /api/v1/bookings/summary`, SR-24
