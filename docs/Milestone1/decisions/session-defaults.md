---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [auth, security, config]
repos: [rentxe]
---

# ADR — Spring's session defaults: 30 minutes idle, 14 days with remember-me

Context: With Spring Security sessions ([login-auth-approach](login-auth-approach.md)) we had to choose how long a login lasts, where sessions are stored and which remember-me cookie to use.
Decision: Keep LOGIN-17. "Keep me logged in" (ticked by default) lasts 14 days; unticked, the login ends when the browser closes or after 30 minutes without a request. Sessions are kept in the app's memory. Remember-me uses Spring's signed cookie (`TokenBasedRememberMeServices`), with its key from `RENTXE_REMEMBER_ME_KEY`.
Why: These are Spring's defaults, so there is almost nothing to configure and no extra tables. The signed cookie already stops working after a password reset (LOGIN-22) and for suspended accounts (LOGIN-16). Most users keep the box ticked, so a restart barely affects them. If a session ends mid-task, the user logs in again and returns with `?next=` (LOGIN-29).
Rejected:
- 2 hours idle: fewer surprise log-outs, but longer exposure on shared computers.
- Spring Session JDBC and a `persistent_logins` table: sessions survive restarts and single devices can be logged out, but that is two tables and a dependency the MVP doesn't need.
Trade-off: a restart or redeploy logs out users who didn't tick "Keep me logged in".
Links: SRS §2.1, §3.2 · [api/login.md](../api/login.md) LOGIN-16, LOGIN-17, LOGIN-22, Q17
