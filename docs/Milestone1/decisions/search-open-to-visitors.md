---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [search, vehicle, auth, ui]
repos: [rentxe]
---

# ADR — Search and vehicle pages work logged out

Context: The search and vehicle endpoints were already Public, and the landing page's search form opens the search page, but the search mockup only shows the logged-in customer nav. Nobody had decided whether the pages themselves need a login.
Decision: Anyone can use the search and vehicle pages. Logged out, the nav is the landing page's: logo, Help, theme toggle, Log in and Sign up, with `?next=` back to the current page. Only **Request to book** needs a `CUSTOMER` login. A logged-out visitor who clicks it goes to `/login?next=<the vehicle page URL>` and, after log in or sign-up, is back on the same vehicle with the same dates. Nothing is sent by itself; they click again.
Why: Visitors can try RentXe before signing up, shared links work, and it matches the Public API and the landing hand-off. Asking for a login at the moment of booking, then returning to the same vehicle, loses nothing the visitor picked.
Rejected:
- A login wall on the search page: the landing page's search form would end at a login form, and most visitors would leave.
Trade-off: a second nav state to mock up (`?user=guest` on search and vehicle).
Links: SRS §2.1, §2.3 · [api/search.md](../api/search.md) SR-25, Q6 · [api/vehicle.md](../api/vehicle.md) VEH-39, Q16 · [api/login.md](../api/login.md) LOGIN-29 · [api/README.md](../api/README.md) team decision 8
