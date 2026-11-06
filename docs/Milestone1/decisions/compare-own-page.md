---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [search, ui]
repos: [rentxe]
---

# ADR — Comparison opens its own page

Context: The brief's feature area is "Vehicle Search and Comparison". The search page has Compare ticks, a tray of up to 3 vehicles and a compare endpoint, but the page the tray's button opens had no design.
Decision: Comparison stays in the MVP and has its own page, `/compare?ids=1,3&from=…&to=…&placeId=…`, with one column per vehicle in tick order: photo, price and estimated total, company and rating, specs, distance, availability for the dates, and a View button each. It loads with `GET /api/v1/vehicles/compare`.
Why: The link can be shared and reloaded like a search, the endpoint is already designed, and there is room for more rows later.
Rejected:
- A side-by-side panel on the search page: cramped on phones, hard to share, and it complicates the tray.
- No comparison in the MVP: it leaves out half of a core feature area.
Trade-off: one more page to mock up; it may add fields to the compare response (deposit, cover options, pick-up address) once designed.
Links: SRS §2.3, §5 · [api/search.md](../api/search.md) SR-20, endpoint 3, Q15 · [api/README.md](../api/README.md) Not covered yet
