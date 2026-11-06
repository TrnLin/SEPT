---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [search, ui]
repos: [rentxe]
---

# ADR — The motorbike engine filter adds "Over 160 cc"

Context: The Engine size filter offered Any, ≤ 125 cc and 126–160 cc. A bigger bike, for example 300 cc, matched only Any, and nobody could filter for big bikes.
Decision: The options are fixed: Any, ≤ 125 cc (`maxEngineCc=125`), 126–160 cc (`minEngineCc=126&maxEngineCc=160`) and Over 160 cc (`minEngineCc=161`). No API change.
Why: Every motorbike fits exactly one option. 125 cc is the usual learner and small-scooter limit, 126–160 cc covers the common bigger scooters, and over 160 cc covers touring bikes.
Rejected:
- Options built from the data: more facet logic, and the options change by city, which is harder to test.
- Leaving it: big bikes can't be filtered for.
Trade-off: in a scooter-heavy city the new option can match nothing. Engine size has no counts, so the visitor only finds out from the empty state, which then suggests removing it (SR-19).
Links: SRS §2.3 · [api/search.md](../api/search.md) SR-11, Q8
