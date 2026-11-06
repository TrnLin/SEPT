---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [search]
repos: [rentxe]
---

# ADR — The Recommended sort: rating minus 0.1 per km

Context: Search's default sort, "Recommended", needed a rule. SR-18 proposed one, with a weight and a default for unreviewed companies that were our own guesses.
Decision: Booked vehicles go last. The rest are ranked by company rating − 0.1 × `distanceKm`, highest first; a company with no reviews counts as 3.0. Ties go to the lower `pricePerDay`, then the lower `id`. The order is the same for every visitor.
Why: One line of code that balances a good company against a close one, with worked examples in SR-18 for tests. New companies still show and can win on the Price and Distance sorts.
Rejected:
- Rating first, distance only for ties: a 4.9 company 19 km away would beat a 4.8 company down the street.
- Also weighing price, review count and reply time: more weights to guess, harder to test and explain.
Trade-off: the 0.1 weight and the 3.0 default are judgement calls. This is not the personalised-recommendations custom feature (SRS §2.7), which would use each customer's history and could later add to this score.
Links: SRS §2.3 · [api/search.md](../api/search.md) SR-18, Q4
