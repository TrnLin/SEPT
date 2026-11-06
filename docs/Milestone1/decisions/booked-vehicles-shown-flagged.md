---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [search, ui, api]
repos: [rentxe]
---

# ADR — Booked vehicles stay in search results, flagged

Context: The search mockup shows vehicles that are booked for part of the searched dates as muted rows with "Booked 11–12 Dec", and counts them in every number. A headline such as "8 vehicles" could include vehicles the customer can't book.
Decision: Booked vehicles stay in the results, flagged, and still count everywhere (SR-9). The search response adds `availableCount`, the number of results free for the dates. When some results are booked, the headline says so: "8 vehicles near Melbourne CBD · 7 free for your dates."
Why: Customers see the full choice and can move their dates to get a vehicle they like; the vehicle page shows its next free dates. The extra count keeps the headline honest at the cost of one number.
Rejected:
- Hide booked vehicles: a vehicle busy one day of a long trip vanishes with no hint, and an empty result gives no reason to try other dates.
- A "Free for my dates only" filter: another filter, more facet counts and another empty-state suggestion. It can come later if testers ask.
Trade-off: the list can show rows the customer can't book for these dates.
Links: SRS §2.3 · [api/search.md](../api/search.md) SR-9, Q3
