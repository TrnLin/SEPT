---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [ui, auth, accessibility, errors]
repos: [rentxe]
---

# ADR — Field errors under the field, other errors in a banner at the top of the form

Context: The login mockup has an error line under each field and a toast that disappears. The API doc assumed log in errors went under Password and server failures in the toast.
Decision: Errors about one field (`400`, `409`) show under that field. Errors that aren't about one field (`401`, `403`, `429`, network errors and `5xx`) show in one error banner at the top of the form, under the heading, with `role="alert"`. It stays until the user edits a field or submits again. A `401` keeps the email, clears the password and moves the focus to it. A `403` links to `/help`. Errors never use the toast.
Why: `401` is deliberately about the email and password together, so showing it under Password suggests the email was right. `403` and `429` aren't about any field. A toast disappears before some users read it and is handled poorly by screen readers.
Rejected:
- Login errors under Password and failures in a toast (the old assumption): the problems above.
- Every error in the toast: errors vanish, the worst option for accessibility.
Applies to other forms too: the same pattern is proposed for every form on the site, such as booking requests and the company dashboard.
Links: SRS §3.3 · [api/login.md](../api/login.md) LOGIN-32, Q15 · [static-help-page](static-help-page.md)
