---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [landing, reviews, api]
repos: [rentxe]
---

# ADR — Landing page reviews are fixed sample content

Context: The landing page shows three review cards. The first draft served them from `GET /api/v1/reviews/featured`.
Decision: The three reviews are fixed text written into the page, and the landing page has no endpoint of its own. The featured-reviews endpoint stays in `landing.md` under "Option for later". If it is ever built, the whole Reviews section and its header and footer links are hidden when the call fails or returns fewer than 3 reviews, with no error shown (LP-11).
Why: The brief's reviews feature only asks that customers can review a finished rental and see feedback on vehicles and companies, and the vehicle page already does both. The Milestone 1 rubric grades process, requirements, the SRS and testing, so static marketing quotes cost no marks. The one condition is that SRS §5 describes them as fixed sample content.
Rejected:
- Featured-reviews API in the MVP: one more endpoint, with its own error states and tests, for no rubric gain.
Links: SRS §2.6, §5 · [api/landing.md](../api/landing.md) LP-11, LP-21 · [one-rating-per-review](one-rating-per-review.md)
