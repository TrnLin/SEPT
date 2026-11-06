---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [auth, email, ui, config]
repos: [rentxe]
---

# ADR — Forgot and reset views on the login page; Spring Mail with Brevo

Context: The reset endpoints were written (LOGIN-20 to LOGIN-22), but the mockup had no screens for them: "Forgot password?" sent the Email field's value at once. Nothing said how emails are sent. Login uses Spring Security sessions ([login-auth-approach](login-auth-approach.md)), so Supabase doesn't send them.
Decision:
- Screens: `?view=forgot` (Email, filled in from the log in form, and **Send reset link**, then an on-page "If an account exists…" message) and `?view=reset&token=…` (New password and **Save password**) on the login page (LOGIN-33).
- Sending: Spring Mail over SMTP, every setting from environment variables (LOGIN-34). Mailpit in Docker on laptops, a fake mail sender in tests, and Brevo's free SMTP relay (300 emails a day, a single verified sender address) when deployed.
Why: A separate forgot step lets users check the email before sending, and the confirmation stays on screen. SMTP settings keep the provider swappable without code. Brevo needs no domain; Mailpit and the fake sender let everyone test the full reset offline.
Rejected:
- Sending straight from the log in form's Email field: an empty or mistyped email fails quietly, and it is easy to click by accident.
- Resend: needs a domain we own before it emails anyone but the account owner. Switch to it later, by changing settings only, if the team buys a domain.
- Gmail app password: ties sending to someone's personal account.
- Logging the link only: the demo couldn't show a real email.
Risk: emails from a free-mail sender address (for example Gmail) may land in spam. Use a sender the team controls if possible, and check the spam folder in the demo.
Links: SRS §2.1, §3.2 · [api/login.md](../api/login.md) LOGIN-20 to LOGIN-22, LOGIN-33, LOGIN-34, Q4 · [architecture/tech-decisions.md](../architecture/tech-decisions.md) Email
