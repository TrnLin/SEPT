---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [api, srs, docs]
repos: [rentxe]
---

# ADR — Document the API per mockup page

Context: We have mockups for the landing, login, search and vehicle pages, but no written backend schema. The SRS needs requirements that match those screens.
Decision: One file per page in `docs/Milestone1/api/` (`landing.md`, `login.md`, `search.md`, `vehicle.md`). `api/README.md` holds the shared conventions, the shared models and an index of every endpoint. Each page's business rules are numbered (LP-, LOGIN-, SR-, VEH-).
Why: Each file sits next to its screen, so a mockup change shows which endpoints change with it. The SRS requirements and acceptance criteria can cite rule IDs instead of repeating the rules. Where two pages overlap, the README holds the single shared definition (for example the SearchResult card and `startDate`/`endDate`).
Rejected:
- Not discussed. The structure came from the request "the API schema needed for each page".
Links: SRS §2, §4, §5 · [api/README.md](../api/README.md) · [api/schema-review.html](../api/schema-review.html)
