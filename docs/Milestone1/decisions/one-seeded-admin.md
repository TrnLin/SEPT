---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [auth, admin, security, config]
repos: [rentxe]
---

# ADR — One seeded admin for the MVP; admins can promote others later

Context: Sign-up only creates customer and company accounts, so that nobody can make themselves an admin. Admin accounts still have to come from somewhere.
Decision: In the MVP there is exactly one admin. When Spring starts and no `ADMIN` account exists, it creates one from the settings `RENTXE_ADMIN_EMAIL`, `RENTXE_ADMIN_PASSWORD` and `RENTXE_ADMIN_NAME`. The password is never committed: it comes from an environment variable or a git-ignored local file. An existing admin is never overwritten. The dev and test profiles may seed a known admin for demos and tests; production never does. Later, not in the MVP, the original admin will be able to make other accounts admins.
Why: One admin is enough for the MVP and the demo, and no screen or endpoint can create an admin, which is the safest starting point. Promoting accounts later covers the need for more admins without a separate admin sign-up.
Rejected for now:
- An "Add admin" form: an extra screen and endpoint the MVP doesn't need.
- Promoting accounts in the MVP: deferred, see below.
Questions for the later feature:
- Can only the original (seeded) admin promote others, or any admin? Only the original means User needs a flag such as `owner`.
- Which accounts can be promoted? Probably customers only, because a company account is tied to its Company.
- What happens to a promoted customer's bookings and reviews? A fresh account per admin avoids mixing them, and fits [one role per account](one-role-per-account.md): promoting would replace the role, not add one.
- Can an admin be demoted or suspended, and who may do it? The original admin must never be removable.
Links: SRS §2.1, §3.2 · [api/login.md](../api/login.md) LOGIN-9, Q10
