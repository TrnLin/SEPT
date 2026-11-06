---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [auth, ui]
repos: [rentxe]
---

# ADR — A logged-in user who opens the login page is sent on

Context: The mockup only shows the login form. Nothing said what a user who is already logged in sees when they open `/login`, for example from a bookmark, the back button or a link in an email.
Decision: The login page calls `GET /api/v1/auth/me` on load. If the user is logged in, it sends them where a fresh log in would (role, LOGIN-28, `next`) without showing the form. If not, or if the call fails, it shows the form. To switch accounts, a user logs out first.
Why: A login form is of no use to someone already logged in, and this is what most sites do. It needs no new screen, and it lets `next` work for a customer whose session is still alive. It matches the landing decision in spirit: show each visitor the page that is useful to them.
Rejected:
- Always show the form: logging in again silently replaces the session, which is confusing.
- An "already logged in" card with Continue and Log out: easier account switching, but a new mockup state for a rare case.
Links: SRS §2.1 · [api/login.md](../api/login.md) LOGIN-13, LOGIN-28, LOGIN-29, LOGIN-30 · [logged-in-landing-same-page](logged-in-landing-same-page.md)
