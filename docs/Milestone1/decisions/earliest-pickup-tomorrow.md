---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [booking, search, landing, vehicle]
repos: [rentxe]
---

# ADR — The earliest pick-up is tomorrow

Context: Every booking waits for the rental company to approve it. One landing review said "picked it up the same afternoon", and the vehicle calendar lets you click today.
Decision: A rental can start tomorrow at the earliest, on every page (LP-3, SR-4, VEH-3). The review now says "picked it up the next morning". The vehicle calendar must stop offering today.
Why: A same-day start would need companies to approve within hours, and we would have to define what happens when they don't answer in time. Changing the quote is the cheaper fix, because the reviews are fixed text ([static-landing-reviews](static-landing-reviews.md)).
Rejected:
- Allow same-day pick-up: it changes the date rules on three pages and adds the "no answer in time" case.
Links: SRS §2.4, §2.8 · LP-3, SR-4, VEH-3 · [api/landing.md](../api/landing.md) Q7 · api/README.md team decision 2
