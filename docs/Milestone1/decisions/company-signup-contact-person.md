---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [auth, signup, company, data-model, admin]
repos: [rentxe]
---

# ADR — Company sign-up asks for the registering person's name and a phone number

Context: The company sign-up form asked only for the company name, email and password. Admins must verify a company before its vehicles appear in search (api/README.md team decision 5), but that gave them nothing to check. The login's `fullName` also had to hold the company name, so the account menu showed a company where a person's name and initials go.
Decision: Company sign-up also asks for "Your name" (`fullName`, stored on the User, the login) and "Phone" (`phone`, stored on the Company). The person is whoever fills in the form, for example a manager, not a separate account or outside vendor. It stays one login per company. The phone has 8 to 15 digits and is stored without spaces (LOGIN-25). Only the company itself and admins can see it.
Why: Two extra fields give the admin someone to phone before verifying, and the account menu shows a real person ("Lan Nguyen · Company account"). The form stays short.
Rejected:
- Keep three fields: verifying would be a click on trust, and `fullName` would keep holding the company name.
- Also ask for ABN and business address: lets the admin check the public ABN register, but doubles the form and the validation before a company can look around. The company profile page can ask for them later.
- Several staff logins per company: a bigger feature, left out of the MVP. The model allows it later through `User.companyId`.
Links: SRS §2.1 · [api/login.md](../api/login.md) Q1, `POST /api/v1/auth/register/company`, LOGIN-7, LOGIN-25 · Company and User models in [api/README.md](../api/README.md)
