---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [ui, static-pages, auth, help]
repos: [rentxe]
---

# ADR — A static /help FAQ page for every visitor

Context: The login footer links to Help, Terms and Privacy. Terms and Privacy already have static pages (LP-25); Help went nowhere.
Decision: Help opens `/help`, a static FAQ page with no API. It is written for every visitor, not for companies: **Your account** (signing up, forgot password, Keep me logged in, one role per email), **Renting** (how a booking moves from request to review, earliest pick-up tomorrow, the cancellation rule, no payment through RentXe, bring your licence) and **Contact** (the support email). Company questions get one line linking to `/for-companies`.
Why: People who are stuck get answers on the spot instead of waiting for an email. Keeping it generic avoids repeating `/for-companies`, which already covers the company side.
Rejected:
- The support email only: no new page, but every simple question becomes an email.
- Removing Help: leaves stuck visitors with no way out.
- A help page aimed at companies: `/for-companies` already does that.
Follow-up: the answers repeat decided rules (LP-3, VEH-22, VEH-23, LOGIN-4), so they must be updated when those rules change.
Links: SRS §5 (wireframe) · [api/login.md](../api/login.md) LOGIN-31, Q14 · [static-company-legal-pages](static-company-legal-pages.md)
