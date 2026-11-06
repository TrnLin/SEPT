---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [auth, security, api, frontend]
repos: [rentxe]
---

# ADR — Keep Spring's CSRF protection with a token cookie and header

Context: Login uses session cookies ([login-auth-approach](login-auth-approach.md)), which the browser sends on every request to our site, even one triggered by another site. Spring Security blocks such cross-site request forgery by default, so we had to set it up for a page that calls a JSON API, or turn it off.
Decision: CSRF protection stays on for `/api/**` (LOGIN-36). Spring sets a readable `XSRF-TOKEN` cookie (`CookieCsrfTokenRepository.withHttpOnlyFalse()`), and a shared `api()` wrapper around `fetch` copies it into the `X-XSRF-TOKEN` header on every `POST`, `PATCH`, `PUT` and `DELETE`. A new `GET /api/v1/auth/csrf` (Public, `204`) gives the page a token before its first `POST`. Missing or wrong tokens get `403`.
Why: It is Spring's default protection, so we keep it rather than argue for turning it off. The cost is one wrapper, written once, and one small endpoint. It gives SRS §3.2 something concrete to show and test (`.with(csrf())` in MockMvc).
Rejected:
- Turning CSRF off and relying on `SameSite=Lax` cookies: relies only on browser behaviour, misses attacks from our own subdomains and older browsers, and looks like a gap in a security review.
Assumption: the pages and the API share one origin. Spring serves the pages, or, if the team picks React with its own dev server, that server proxies `/api` to Spring. Otherwise cookies need CORS setup whichever option we choose.
Links: SRS §3.2 · [api/login.md](../api/login.md) GET /auth/csrf, LOGIN-36, Q5 · [api/README.md](../api/README.md) CSRF, Origin
