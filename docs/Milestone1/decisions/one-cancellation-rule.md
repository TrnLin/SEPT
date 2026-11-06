---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [booking, fees, landing]
repos: [rentxe]
---

# ADR — One cancellation rule for every company

Context: "How it works" step 03 said customers can cancel "where their rules allow", which suggests a policy per company. `vehicle.md` already defines one rule. The brief says "where permitted" and leaves the rule to us.
Decision: The same rule for every company: cancelling is free until 24 hours before pick-up, then the fee is 50% of `totalPrice` (A$102 on the A$204 Corolla example). Step 03 now reads "…and you can cancel free until 24 hours before pick-up." Payment is out of scope, so the fee is recorded on the booking, not charged.
Why: There is one rule to write in the SRS and one set of tests, and customers see the same terms on every vehicle.
Rejected:
- A rule per company: it needs new Company fields, a setting on the company profile page, and the quote and cancel flows reading each company's rule. If the team wants it later, 3 presets (Flexible, Standard, Strict) are the cheapest version.
Links: SRS §2.8 · [api/vehicle.md](../api/vehicle.md) VEH-22, VEH-23 · [api/landing.md](../api/landing.md) Q4 · api/README.md team decisions 7 and 9
