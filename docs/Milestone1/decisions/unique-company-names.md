---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [company, signup, data-model, search]
repos: [rentxe]
---

# ADR — Company names are unique, ignoring case and extra spaces

Context: Customers choose a company by its name on the search and vehicle pages, and reviews build up under that name. LOGIN-11 assumed unique names without the team confirming it.
Decision: Company names are unique. Two names clash if they match after trimming, turning runs of spaces into one, and ignoring case. A clash returns `409` on `companyName`: "A company with this name is already registered." The name is stored as typed (trimmed). Suspended companies keep their name, and the same rule applies to renames later. A unique index on the normalised name enforces it in Postgres.
Why: Two companies with the same name can't be told apart in search, and a copycat could borrow a well-reviewed company's name. One index prevents both. Company names are public, so the error message leaks nothing private.
Rejected:
- Not unique, with admins catching copies when verifying: search would still show identical names, and it relies on the admin noticing.
- Unique on the exact text only: "Saigon Wheels" and "saigon wheels" would both get through.
Trade-off: two real businesses with the same name in different cities can't both use it; the second adds something, such as a suburb.
Links: SRS §2.1 · [api/login.md](../api/login.md) LOGIN-11, Q12 · [api/README.md](../api/README.md) Company.name
