---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [reviews, data-model, landing]
repos: [rentxe]
---

# ADR — One rating per review, for the vehicle and the service together

Context: The landing copy said "customers rate the vehicle and the company", which suggests two scores per rental. The Review model has a single `rating` from 1 to 5.
Decision: Keep one `rating` per review. It scores the whole rental, the vehicle and the service together, and the same number counts toward the vehicle's average and the company's average. The reviews intro now reads "customers give one rating for the vehicle and the service together".
Why: It is the least work: one star row on the form, and each average comes straight from the reviews. It still meets the brief's "view feedback about vehicles and rental companies". The cost is that "great car, rude staff" becomes one middle score.
Rejected:
- Two ratings (`vehicleRating` and `companyRating`): a fairer split, but it adds a second star row, a second average and more test cases. Worth revisiting if the company page needs its own score.
Links: SRS §2.6 · Review model in [api/README.md](../api/README.md) · [api/landing.md](../api/landing.md) Q3 · api/README.md team decision 6
