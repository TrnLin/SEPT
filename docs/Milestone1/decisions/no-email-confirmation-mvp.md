---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [auth, email, signup]
repos: [rentxe]
---

# ADR — No email confirmation in the MVP

Context: Nothing in the mockup asks new users to confirm their email, and the team had to decide whether accounts should work before the email is confirmed.
Decision: Accounts work as soon as sign-up succeeds. No confirmation email, no confirm view and no `User.emailVerifiedAt` field (LOGIN-35).
Why: It keeps sign-up simple. Companies already get a human check, because an admin phones them before verifying (LOGIN-26). Customers can't do harm alone, because every booking needs the company's approval. A required confirmation would also lock people out, the marker included, whenever an email from Brevo lands in spam.
Rejected:
- Must confirm before logging in: the most friction and work, and spam filters could lock users out.
- Soft confirmation (account works, booking requests need a confirmed email): a good later upgrade. It reuses the reset email and token pattern (LOGIN-33, LOGIN-34), but isn't needed for the MVP.
Trade-off: a mistyped email is only noticed when a reset link doesn't arrive.
Links: SRS §2.1 · [api/login.md](../api/login.md) LOGIN-35, Q9 · [password-reset-views-and-email](password-reset-views-and-email.md)
