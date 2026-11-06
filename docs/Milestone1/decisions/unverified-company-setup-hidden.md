---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [auth, company, admin, search, vehicle]
repos: [rentxe]
---

# ADR — Unverified companies can set up but stay hidden; rejecting means suspending

Context: A company starts with `verified: false`, and only verified companies appear in search (api/README.md team decision 5). Nothing said what a company can do while it waits, or how an admin rejects one. Company has no status of its own.
Decision: A company is live when its Company is `verified` and its account is `ACTIVE`. Before an admin verifies it, the company can log in, edit its profile and add vehicles, but none of it is public. Its vehicles are left out of search, return `404` on public vehicle endpoints and cannot be requested, and its dashboard says "Waiting for verification". Once verified, all its listed vehicles go live at once. There is no "rejected" state: the admin suspends the company's account, which also takes a verified company's vehicles out of search.
Why: The company sets up while it waits, so its listings go live the moment it is approved, and customers never see an unchecked company. Reusing the User `SUSPENDED` status means one mechanism instead of a new Company status.
Rejected:
- Lock the company out until verified: it can only start adding vehicles after approval, and every company endpoint needs an extra check.
- No verification: simplest, but the admin can only react after a bad listing is already public, which conflicts with the "Verified rental companies" claim on the landing page (LP-12).
- A `REJECTED` or Company `status` field: a second mechanism that does what suspending the account already does.
Follow-up: the admin page needs a list of companies waiting for approval (name, contact person, phone) and a verify endpoint, for example `PATCH /api/v1/admin/companies/{id}`. Seed data starts the demo companies as verified.
Links: SRS §2.1, §2.8 · [api/login.md](../api/login.md) Q2, LOGIN-26, LOGIN-27 · [api/search.md](../api/search.md) SR-2, Q5 · [api/vehicle.md](../api/vehicle.md) VEH-17, VEH-35 · api/README.md team decision 5
