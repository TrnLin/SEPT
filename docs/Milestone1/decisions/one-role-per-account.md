---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [auth, data-model, security, roles]
repos: [rentxe]
---

# ADR — One role per account

Context: The team asked whether one account could be a customer, a company and an admin at the same time.
Decision: No. Each account has exactly one role (`CUSTOMER`, `COMPANY` or `ADMIN`), set at sign-up, and no endpoint changes it. Someone who rents and also runs a company uses two accounts with two emails (LOGIN-4).
Why: One role keeps `User.role` a single value, gives every role one home page after log in (LOGIN-13, LOGIN-28), and needs no conflict rules. With several roles we would need rules against booking or reviewing your own company's vehicles and against an admin verifying their own company. Suspending a company (LOGIN-27) would also lock the person out of renting, which would bring back a separate Company status. Every endpoint would also need tests for role combinations.
Rejected:
- Any combination of roles: needs all the rules above, and an admin combined with another role breaks separation of duties.
- Customer and company on one account, as on Airbnb: a reasonable later feature, not needed for the MVP. It would need a `user_roles` table, a "Switch to company / customer view" item in the account menu, a rule against booking your own company's vehicles, and a status per role.
Later: if customer + company on one account is added, admin still stays a separate account. Promoting someone to admin ([one-seeded-admin](one-seeded-admin.md)) should use a fresh account.
Links: SRS §2.1, §3.2 · [api/login.md](../api/login.md) LOGIN-4, LOGIN-27, Q11 · [api/README.md](../api/README.md) User.role
