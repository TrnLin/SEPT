---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [landing, auth, ui]
repos: [rentxe]
---

# ADR — Logged-in visitors see the same landing page

Context: The landing mockup only showed the logged-out header. Nothing said what a logged-in user sees when they open `/` from a bookmark, a typed address or an email link.
Decision: The page is the same for everyone and nothing redirects. **Log in** and **Sign up** become the account menu, with the visitor's initials and first name from `GET /api/v1/auth/me`. Customers get the same menu as the search page. Companies also get **Dashboard** and admins get **Admin**, an assumption until those pages are mocked up. Every menu has **Log out**. The mockup previews it with `?user=customer|company|admin`.
Why: It is one rule to write and test, nobody is moved somewhere they didn't expect, and it needs no new API. Logged-in customers rarely reach `/` by clicking, because the logo on the search page already links to Search.
Rejected:
- Redirect by role (customer to Search, company to Dashboard, admin to Admin): three rules to test, and the move is unexpected.
- Mix (customers stay, companies and admins are redirected): still three rules.
Links: SRS §5 · [api/landing.md](../api/landing.md) LP-24, Q5 · [api/login.md](../api/login.md) `GET /auth/me`
