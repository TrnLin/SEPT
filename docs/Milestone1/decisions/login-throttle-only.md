---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [auth, security, email]
repos: [rentxe]
---

# ADR — One throttle: failed log ins, 15 minutes

Context: Two throttling rules were proposed: LOGIN-23 for failed log ins and LOGIN-24 for reset emails. A third, a per-IP cap on reset requests, was suggested to protect Brevo's 300 emails a day.
Decision: Keep it simple, with one rule. After 5 failed log ins for one email from one IP address within 15 minutes, log in for that email and IP returns `429` with `Retry-After` for 15 minutes, even with the correct password (LOGIN-23). Counters live in the app's memory, for example a Caffeine cache, and clear after 15 minutes. No limit on reset emails: LOGIN-24 is dropped.
Why: Password guessing is the main threat and the one SRS §3.2 is most likely to ask about. One counter is quick to build and test (5 bad attempts, then the 6th gets `429`). The key is email + IP, so an attacker can't lock a real user out of their own connection.
Rejected:
- Also limiting reset emails per address and per IP: more counters than the MVP needs.
- No throttling: unlimited password guessing.
Known risks: someone could flood one inbox with reset emails, or use up Brevo's daily allowance so real resets fail until the next day. If that happens, add the dropped limits. Counters reset when the app restarts and aren't shared between copies, which is fine with one container.
Links: SRS §3.2 · [api/login.md](../api/login.md) LOGIN-23, LOGIN-24, Q8 · [password-reset-views-and-email](password-reset-views-and-email.md)
