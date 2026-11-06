---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [search, vehicle, company, ui]
repos: [rentxe]
---

# ADR — Companies and admins use search with their own menu, and companies can edit their vehicles from it

Context: Search and vehicle pages are public, so a logged-in company or admin can open them, but the mockups only show the customer nav, and only customers can send booking requests.
Decision: Companies and admins see the same pages with their own account menu, as on the landing page (Dashboard or Admin, then Log out; no My bookings). On a company's own vehicles, search rows, the map card and the compare tray show an **Edit** button, and the vehicle page shows **Edit vehicle** in place of **Request to book**. Both open the company's vehicle form (assumed at `/company/vehicles/{id}/edit`) with `next` set to the current page, so the company comes back after saving. Other companies and admins see "Only customer accounts can book".
Why: A company can check how its listings look next to others and fix one on the spot, without going back to its catalogue to find it. Admins can see what customers see. The page already has `company.id` on each row and `companyId` from `GET /auth/me`, so no API change is needed.
Rejected:
- Redirect companies and admins to their dashboard: they couldn't see search as customers do.
Trade-off: role checks in the nav, on each row and on the booking panel. The edit endpoint must still check ownership itself; the button is only a link.
Links: SRS §2.2, §2.3 · [api/search.md](../api/search.md) SR-26, Q12 · [api/vehicle.md](../api/vehicle.md) VEH-40 · [api/landing.md](../api/landing.md) LP-24 · [api/login.md](../api/login.md) LOGIN-29
