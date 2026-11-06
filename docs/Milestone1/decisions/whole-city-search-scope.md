---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [search]
repos: [rentxe]
---

# ADR — Search covers the whole city of the picked place

Context: When a customer picks "Melbourne CBD", search had to decide which vehicles count as near: the whole city, a fixed radius, or only that area.
Decision: Search shows every vehicle in the picked place's city (SR-2). The place only sets the point that distances, the Distance sort, the 2 / 5 / 10 km filter and the map centre are measured from. The Where list keeps cities, areas and airports for that reason: "Melbourne Airport" shows all Melbourne vehicles, nearest to the terminal first.
Why: With a few dozen vehicles per city, the whole city is the useful scope and results are never empty just because the nearest car is 11 km away. It is a simple city match, and later open search (any address) only needs the address's city.
Rejected:
- A fixed radius such as 25 km: edge suburbs fall in or out depending on the place, and it needs a distance query in the database.
- The area only: mostly empty results with a small fleet.
Trade-off: "near Melbourne CBD" also lists a car at the airport, 19.5 km away; the distance on each row and the km filter make that clear.
Links: SRS §2.3 · [api/search.md](../api/search.md) SR-2, SR-3, Q7, Q13 · [fixed-place-list](fixed-place-list.md)
