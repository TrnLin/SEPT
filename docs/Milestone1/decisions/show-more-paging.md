---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [search, ui]
repos: [rentxe]
---

# ADR — Search results load 10 at a time with "Show more"

Context: The search mockup shows 8 results and no paging control. The API already pages with `page` and `size`; the page needed a control.
Decision: The list shows 10 rows, then a "Show 10 more · 20 of 48" button adds the next 10 below. At the end, the "End of results" line replaces it. Changing filters, sort, place or dates starts again from the top. `page` is not kept in the URL. The map still loads up to 100 pins in one call.
Why: Easy on phones, the customer keeps their place, and ticks and the compare tray stay put. One city has at most a few hundred vehicles, so customers rarely go deep.
Rejected:
- Numbered pages: fiddly on phones, and each page replaces the list.
- Infinite scroll: the footer and "End of results" become hard to reach, and it is harder for screen readers and tests.
Trade-off: a reload or shared link shows the first 10 rows again. Revised 2026-11-07 from 20 to 10 rows a page, so the first screen stays short.
Links: SRS §2.3 · [api/search.md](../api/search.md) SR-22, Q10
