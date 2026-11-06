# Log in and sign up

One page to log in, sign up as a renter or a rental company, and ask for a password reset. Admins log in here too.

| | |
|---|---|
| Mockup | `assets/mockups/login/index.html` |
| SRS area | 2.1 User and Profile Management |
| Owns | Every endpoint under `/api/v1/auth/*` |

## Page states

| URL | View | Account type | Title | Submit button |
|---|---|---|---|---|
| `login/` | Log in | Renter | Welcome back. | Log in |
| `login/?as=company` | Log in | Rental company | Back to your fleet. | Log in |
| `login/?view=signup` | Sign up | Renter | Start riding. | Create account |
| `login/?view=signup&as=company` | Sign up | Rental company | List your fleet. | Register company |

- Any other `view` value means log in. Any other `as` value means renter.
- Switching the view or account type rewrites the URL without a reload.
- The landing page links to all four states. The customer nav's "Log out" link ends here too.
- Other states: field errors (shown on submit, then updated as the user types), a busy button ("Logging in…", "Creating account…"), and a toast.
- There is no admin tab. An admin can log in with either tab selected.

## What the page shows

| UI element | View | Source |
|---|---|---|
| Side panel statement and booking tracker | Both | Static copy that changes with the account type. No data. |
| Renter / Rental company toggle | Both | URL `as`. Sign up: picks the endpoint (`register/customer` or `register/company`). Log in: changes the copy only and sends nothing (LOGIN-13). |
| Full name / Company name | Sign up | Renter: `fullName` on `POST /api/v1/auth/register/customer`. Company: `companyName` on `POST /api/v1/auth/register/company`. |
| Email | Both | `email` on log in and both register endpoints |
| Password, Show / Hide | Both | `password`. Show / Hide is client-only. |
| "At least 8 characters." | Sign up | Static hint for LOGIN-5 |
| Keep me logged in (ticked by default) | Log in | `rememberMe` on `POST /api/v1/auth/login` |
| Forgot password? | Log in | `POST /api/v1/auth/forgot-password` with the Email field's value |
| I agree to the Terms and Privacy policy | Sign up | `acceptTerms` on both register endpoints |
| Terms, Privacy, Help links | Both | Static pages, no API |
| "Admins log in here too." | Both | Static |
| After success | Both | Redirect by `role` in the response (table below) |
| Page load (assumption, not in the mockup) | Both | `GET /api/v1/auth/me`. `200`: already logged in, so redirect by role. `401`: show the form. |

Where server errors appear. The mockup only has per-field error slots and a toast, so this mapping is an assumption:

| Server error | Shown |
|---|---|
| `errors[].field` is `fullName` or `companyName` | Under Full name / Company name |
| `errors[].field` is `email`, `password` or `acceptTerms` | Under that field or the checkbox |
| `401`, `403` or `429` from log in | `detail` under Password |
| Network error or `5xx` | Toast: "Something went wrong. Try again." |

Where the user goes after log in or sign up:

| `role` | Goes to | Source |
|---|---|---|
| `CUSTOMER` | My bookings | Mockup toast: "this would open your bookings" |
| `COMPANY` | Company dashboard | Mockup toast: "this would open the rental company dashboard" |
| `ADMIN` | Admin dashboard | Assumption. The mockup only says admins log in here. |

None of these pages has a mockup yet.

## Endpoints

| Method | Path | Access | Success |
|---|---|---|---|
| `POST` | `/api/v1/auth/register/customer` | Public | `201` + CurrentUser |
| `POST` | `/api/v1/auth/register/company` | Public | `201` + CurrentUser |
| `POST` | `/api/v1/auth/login` | Public | `200` + CurrentUser |
| `POST` | `/api/v1/auth/logout` | Public | `204` |
| `GET` | `/api/v1/auth/me` | `CUSTOMER`, `COMPANY`, `ADMIN` | `200` + CurrentUser |
| `POST` | `/api/v1/auth/forgot-password` | Public | `204` |
| `POST` | `/api/v1/auth/reset-password` | Public | `204` |

All are in SRS 2.1. CurrentUser is defined under [`GET /api/v1/auth/me`](#get-apiv1authme).

**Two register endpoints, not one with a role field.** The server sets the role from the path. A client can never ask for `ADMIN`, and there is no role value to validate or reject. Each request body is a plain DTO with Bean Validation annotations, so no field is "required only when role is X". Company sign-up will likely gain fields (see Open questions) without touching customer sign-up. The page already knows which one to call from the toggle.

**No "is this email taken" endpoint.** The mockup checks fields on submit, not as the user types. A public check would let anyone test which emails have accounts. The register endpoints return `409` on `email` instead.

### POST /api/v1/auth/register/customer

Creates a `CUSTOMER` account and logs it in.

**SRS:** 2.1 · **Access:** Public

| Name | Type | Required | Rules |
|---|---|---|---|
| `fullName` | string | yes | Trimmed. 1 to 100 characters (LOGIN-7). |
| `email` | string | yes | Trimmed and lower-cased. Valid format, at most 254 characters, not already used (LOGIN-2 to LOGIN-4). |
| `password` | string | yes | 8 to 72 characters. Not trimmed (LOGIN-5). |
| `acceptTerms` | boolean | yes | Must be `true` (LOGIN-8). |

```http
POST /api/v1/auth/register/customer
Content-Type: application/json

{
  "fullName": "Minh Tran",
  "email": "Minh.Tran@example.com",
  "password": "carlton-2026",
  "acceptTerms": true
}
```

`201 Created`

```json
{
  "id": 42,
  "fullName": "Minh Tran",
  "email": "minh.tran@example.com",
  "role": "CUSTOMER",
  "status": "ACTIVE",
  "companyId": null,
  "createdAt": "2026-11-06T08:30:00Z",
  "company": null
}
```

**Cookies:** sets the session cookie `JSESSIONID` (`HttpOnly`). No remember-me cookie, because sign-up has no "Keep me logged in" (LOGIN-12).

| Status | When |
|---|---|
| `400` | A field breaks a rule. One `errors` entry per field. |
| `409` | The email is already used by any account (LOGIN-4). |

```json
{
  "type": "about:blank",
  "title": "Bad Request",
  "status": 400,
  "detail": "Validation failed",
  "instance": "/api/v1/auth/register/customer",
  "errors": [
    { "field": "password", "message": "must be at least 8 characters" },
    { "field": "acceptTerms", "message": "must be accepted" }
  ]
}
```

```json
{
  "type": "about:blank",
  "title": "Conflict",
  "status": 409,
  "detail": "An account with this email already exists",
  "instance": "/api/v1/auth/register/customer",
  "errors": [{ "field": "email", "message": "is already registered" }]
}
```

Notes:
- The `409` carries `errors` so the page can show it under Email.
- Checks run in order: `400` first, then `409`. Nothing is saved on any error.
- If the request comes with a session, the new account's session replaces it.
- The response does reveal that an email is registered. Every sign-up form does this. LOGIN-23 limits how fast anyone can probe.

### POST /api/v1/auth/register/company

Creates a `COMPANY` account and its Company, then logs the account in.

**SRS:** 2.1 · **Access:** Public

| Name | Type | Required | Rules |
|---|---|---|---|
| `companyName` | string | yes | Trimmed. 1 to 100 characters (LOGIN-7). Unique, ignoring case (LOGIN-11, assumption). |
| `email` | string | yes | As for customer sign-up |
| `password` | string | yes | As for customer sign-up |
| `acceptTerms` | boolean | yes | Must be `true` |

```http
POST /api/v1/auth/register/company
Content-Type: application/json

{
  "companyName": "Saigon Wheels Co.",
  "email": "hello@saigonwheels.example",
  "password": "fleet-district1",
  "acceptTerms": true
}
```

`201 Created`

```json
{
  "id": 57,
  "fullName": "Saigon Wheels Co.",
  "email": "hello@saigonwheels.example",
  "role": "COMPANY",
  "status": "ACTIVE",
  "companyId": 7,
  "createdAt": "2026-11-06T08:30:00Z",
  "company": {
    "id": 7,
    "name": "Saigon Wheels Co.",
    "verified": false,
    "rating": null,
    "reviewCount": 0
  }
}
```

**Cookies:** as for customer sign-up.

| Status | When |
|---|---|
| `400` | A field breaks a rule |
| `409` | The email is used (`errors[].field` = `email`), or the company name is taken (`companyName`). Both are listed if both clash. |

Notes:
- Creates one User and one Company in one transaction (LOGIN-10). The Company starts with `verified: false`.
- The mockup asks only for the company name. The User's `fullName` is set to the company name, because there is no person's name to store (see Changes to shared models).
- The customer and company bodies differ only in `fullName` vs `companyName`. Keep them separate so each name matches what it stores.

### POST /api/v1/auth/login

Checks the email and password and starts a session.

**SRS:** 2.1 · **Access:** Public

| Name | Type | Required | Rules |
|---|---|---|---|
| `email` | string | yes | Trimmed and lower-cased before lookup. Valid format. |
| `password` | string | yes | Not blank. The length rule is not checked here. |
| `rememberMe` | boolean | no | Default `false`. The page sends the "Keep me logged in" checkbox, which is ticked by default. |

There is no role field. The Renter / Rental company toggle is not sent (LOGIN-13).

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "minh.tran@example.com",
  "password": "carlton-2026",
  "rememberMe": true
}
```

`200 OK`: CurrentUser, the same body as `GET /api/v1/auth/me`. The page reads `role` and redirects (see the redirect table above).

**Cookies:**

| Cookie | When | Attributes |
|---|---|---|
| `JSESSIONID` | Always. A new ID, even if a session already existed (LOGIN-18). | `HttpOnly`, browser-session lifetime, `Secure` over HTTPS |
| `remember-me` | Only when `rememberMe` is `true` | `HttpOnly`, `Max-Age=1209600` (14 days, Spring's default), `Secure` over HTTPS |

| Status | When |
|---|---|
| `400` | Email is blank or malformed, or password is blank |
| `401` | Wrong password, or no account has this email. The body is the same for both (LOGIN-14). |
| `403` | Correct password, but the account is `SUSPENDED` (LOGIN-15) |
| `429` | Proposal: too many failed attempts (LOGIN-23) |

```json
{
  "type": "about:blank",
  "title": "Unauthorized",
  "status": 401,
  "detail": "Email or password is incorrect",
  "instance": "/api/v1/auth/login"
}
```

```json
{
  "type": "about:blank",
  "title": "Forbidden",
  "status": 403,
  "detail": "This account is suspended. Contact RentXe support.",
  "instance": "/api/v1/auth/login"
}
```

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 900
Content-Type: application/problem+json

{
  "type": "about:blank",
  "title": "Too Many Requests",
  "status": 429,
  "detail": "Too many attempts. Try again in 15 minutes.",
  "instance": "/api/v1/auth/login"
}
```

Notes for Spring Security:
- `formLogin()` reads form fields, not JSON. Use a controller that does four things:
  1. Authenticate with the `AuthenticationManager`.
  2. Change the session ID. Spring's own login filters do this, but a custom controller must do it itself.
  3. Save the context with `HttpSessionSecurityContextRepository`.
  4. When `rememberMe` is `true`, call `RememberMeServices.loginSuccess(...)`. The service normally looks for a `remember-me` request parameter, so set `alwaysRemember(true)` on it and only call it when the box is ticked.
- `DaoAuthenticationProvider` checks account status before the password by default. A wrong password on a suspended account would then return "suspended", which reveals that the email exists. Run the status check after the password check instead, for example in `postAuthenticationChecks`.
- `DaoAuthenticationProvider` already hashes a dummy password for unknown emails, so both `401` cases take about the same time.

### POST /api/v1/auth/logout

Ends the session.

**SRS:** 2.1 · **Access:** Public. Works with or without a session, and always returns `204`.

No request body. `204 No Content`.

**Cookies:** clears `JSESSIONID` and `remember-me` (`Max-Age=0`).

| Status | When |
|---|---|
| none | Always `204` |

Notes:
- Called from the "Log out" item in every logged-in nav. The page then goes to the log in page.
- `POST` only, so another site can't log a user out with a link or an image.
- Spring: `.logout(l -> l.logoutUrl("/api/v1/auth/logout").logoutSuccessHandler(new HttpStatusReturningLogoutSuccessHandler(HttpStatus.NO_CONTENT)).deleteCookies("JSESSIONID"))`. The remember-me service clears its own cookie on logout.

### GET /api/v1/auth/me

Returns the logged-in user. Every logged-in page's nav calls it on load, and public pages can call it to check whether anyone is logged in.

**SRS:** 2.1 · **Access:** `CUSTOMER`, `COMPANY`, `ADMIN`

No parameters.

`200 OK`: CurrentUser

| Field | Type | Notes |
|---|---|---|
| all User fields | | As in the README: `id`, `fullName`, `email`, `role`, `status`, `companyId`, `createdAt` |
| `company` | Company \| null | The full shared Company when `role` is `COMPANY`. Otherwise `null`. |

```json
{
  "id": 42,
  "fullName": "Minh Tran",
  "email": "minh.tran@example.com",
  "role": "CUSTOMER",
  "status": "ACTIVE",
  "companyId": null,
  "createdAt": "2026-11-06T08:30:00Z",
  "company": null
}
```

The company example is the `201` response under [register/company](#post-apiv1authregistercompany).

**Cookies:** if the session has expired but a valid `remember-me` cookie is present, Spring logs the user back in and sets a new `JSESSIONID`. The response is then a normal `200`.

| Status | When |
|---|---|
| `401` | No session and no valid remember-me cookie, or the account was suspended (LOGIN-16) |

```json
{
  "type": "about:blank",
  "title": "Unauthorized",
  "status": 401,
  "detail": "Not logged in",
  "instance": "/api/v1/auth/me"
}
```

Notes:
- The customer nav works these out from the response. They are not extra fields:

  | Nav shows | Derived from | Example |
  |---|---|---|
  | First name | First word of `fullName` | `Minh` |
  | Avatar initials | First letter of the first and last words of `fullName` | `MT` |
  | Account label | `role`: `CUSTOMER` → Customer account, `COMPANY` → Company account, `ADMIN` → Admin account | Customer account |

- The nav's "My bookings 02" count is not part of `/me`. See Open questions.
- An unverified company's dashboard can read `company.verified` to show a "waiting for verification" notice.
- Spring answers unauthenticated requests with a redirect to a login form by default. For `/api/**`, use `HttpStatusEntryPoint(HttpStatus.UNAUTHORIZED)` so the page gets `401`.

### POST /api/v1/auth/forgot-password

Emails a password reset link.

**SRS:** 2.1 · **Access:** Public

| Name | Type | Required | Rules |
|---|---|---|---|
| `email` | string | yes | Trimmed and lower-cased. Valid format. |

```http
POST /api/v1/auth/forgot-password
Content-Type: application/json

{ "email": "minh.tran@example.com" }
```

`204 No Content`, whether or not an account has this email (LOGIN-20).

**Cookies:** none.

| Status | When |
|---|---|
| `400` | Email is blank or malformed |

Notes:
- The mockup sends at once on click ("this would email you a reset link") and has no separate step to enter an email. Assumption: the page sends the Email field's value. If that field is empty or malformed, the page shows the email error and does not call the API.
- After `204`, the page shows a toast that does not confirm the account exists, for example "If an account exists for minh.tran@example.com, we've sent a reset link."
- The email links to the log in page with `?view=reset&token=…`. That view is not in the mockup (see Open questions).
- Email is sent only to `ACTIVE` accounts. Sending happens after the response or off the request thread, so the response time doesn't show whether an email was sent.

### POST /api/v1/auth/reset-password

Sets a new password using the token from the email.

**SRS:** 2.1 · **Access:** Public

| Name | Type | Required | Rules |
|---|---|---|---|
| `token` | string | yes | From the email link. Must exist, be unused and not expired (LOGIN-21). |
| `newPassword` | string | yes | Same rules as `password` at sign-up (LOGIN-5) |

```http
POST /api/v1/auth/reset-password
Content-Type: application/json

{
  "token": "pQ7vR2mX9kL4sT8wZ1yB6nC3dF5gH0jA2eU4iO7rS9t",
  "newPassword": "new-carlton-2026"
}
```

`204 No Content`. The user is not logged in. The page switches to the log in view and shows "Password changed. Log in with your new password."

**Cookies:** none set. Remember-me cookies issued before the reset stop working (LOGIN-22).

| Status | When |
|---|---|
| `400` | `newPassword` breaks a rule, or the token is unknown, used or expired (`errors[].field` = `token`) |

```json
{
  "type": "about:blank",
  "title": "Bad Request",
  "status": 400,
  "detail": "Validation failed",
  "instance": "/api/v1/auth/reset-password",
  "errors": [{ "field": "token", "message": "has expired or was already used" }]
}
```

Notes:
- Unknown, used and expired tokens get the same message.
- Spring's hash-based remember-me (`TokenBasedRememberMeServices`) signs the cookie with the password hash, so a new password breaks old cookies automatically. With `PersistentTokenBasedRememberMeServices`, delete the user's rows in `persistent_logins` instead.

## Endpoints used from other pages

None. The pages users reach after log in (My bookings, company dashboard, admin dashboard) load their own data.

The admin endpoint that suspends an account belongs to the admin page, which is not written yet. LOGIN-15 and LOGIN-16 say what a suspension does to log in.

## Validation and business rules

The mockup gives only "required", the email format and "at least 8 characters". The other numbers here (maximum lengths, token lifetime, throttle limits) are proposals. The team can change them.

| # | Rule | SRS |
|---|---|---|
| LOGIN-1 | The server applies every rule below even when the page has already checked it. A sign-up sent straight to the API with a 7-character password gets `400`. | 2.1, 3.2 |
| LOGIN-2 | Email is trimmed and lower-cased before it is stored or looked up. After signing up as `Minh.Tran@example.com`, logging in as `minh.tran@example.com` succeeds. | 2.1 |
| LOGIN-3 | Email must match `^[^\s@]+@[^\s@]+\.[^\s@]+$` (the page's own check) and be at most 254 characters. Otherwise `400` on `email`. | 2.1 |
| LOGIN-4 | An email can belong to only one account, whatever the role. Signing up with a used email returns `409` on `email` and creates nothing. | 2.1 |
| LOGIN-5 | A password set at sign-up or reset has 8 to 72 characters and at most 72 bytes in UTF-8 (the BCrypt limit). It is not trimmed. A 7-character password gets `400` "must be at least 8 characters". | 2.1, 3.2 |
| LOGIN-6 | Passwords are stored only as BCrypt hashes. No response ever contains a password or a hash. | 3.2 |
| LOGIN-7 | `fullName` and `companyName` are trimmed and must be 1 to 100 characters. A name of only spaces gets `400`. | 2.1 |
| LOGIN-8 | Sign-up needs `acceptTerms: true`. If it is `false` or missing, the response is `400` on `acceptTerms` and nothing is created. The time of acceptance is stored. | 2.1 |
| LOGIN-9 | Sign-up creates only `CUSTOMER` or `COMPANY` accounts, and the endpoint sets the role. No API request can create an `ADMIN`. Admin accounts are seeded when the app starts (assumption). | 2.1, 3.2 |
| LOGIN-10 | Company sign-up creates one `ACTIVE` User with role `COMPANY` and one Company with `verified: false`, linked by `companyId`, in one transaction. If either fails, neither is saved. | 2.1, 2.8 |
| LOGIN-11 | Assumption: company names are unique, ignoring case. Registering "saigon wheels co." when "Saigon Wheels Co." exists returns `409` on `companyName`. | 2.1 |
| LOGIN-12 | A successful sign-up logs the new user in with a session cookie and no remember-me cookie. | 2.1 |
| LOGIN-13 | Log in ignores the Renter / Rental company toggle. The account's role decides where the user goes: `CUSTOMER` to My bookings, `COMPANY` to the company dashboard, `ADMIN` to the admin dashboard. A company logging in with "Renter" selected still reaches the company dashboard. | 2.1 |
| LOGIN-14 | A wrong password and an unknown email return the same `401` status and body. | 3.2 |
| LOGIN-15 | A `SUSPENDED` account cannot log in. With the correct password the response is `403` "suspended". With a wrong password it is the plain `401` from LOGIN-14. No session is created in either case. | 2.1, 2.8 |
| LOGIN-16 | Once an account is suspended, its open sessions and remember-me cookies stop working. Its next request that needs a session gets `401`. | 2.1, 2.8 |
| LOGIN-17 | With "Keep me logged in" ticked, the user stays logged in for 14 days, even after closing the browser. Unticked, the login lasts until the browser closes or 30 minutes pass without a request (Spring Boot's default session timeout). | 2.1 |
| LOGIN-18 | The session ID changes at every log in and sign-up. The `JSESSIONID` before log in differs from the one after. | 3.2 |
| LOGIN-19 | Log out ends the session and clears both cookies. Afterwards, `GET /api/v1/auth/me` returns `401`. Log out accepts `POST` only. | 2.1 |
| LOGIN-20 | Forgot password returns `204` for any well-formed email, whether or not an account has it. A reset email is sent only when an `ACTIVE` account has that email. | 2.1, 3.2 |
| LOGIN-21 | A reset token is 32 random bytes in base64url, and only its hash is stored. It works once and expires 30 minutes after it is issued. Asking for a new link makes the older ones stop working. | 2.1, 3.2 |
| LOGIN-22 | After a reset, the old password fails and the new one works. The token cannot be used again, remember-me cookies issued before the reset stop working, and the reset does not log the user in. | 2.1, 3.2 |
| LOGIN-23 | Proposal: after 5 failed log ins for one email from one IP address within 15 minutes, log in for that email and IP returns `429` with `Retry-After` for 15 minutes, even with the correct password. The same applies to emails that have no account. | 3.2 |
| LOGIN-24 | Proposal: at most 3 reset emails per address per hour. Further requests still return `204` but send nothing. | 3.2 |

## Changes to shared models

Merged into the README on 2026-11-06. Kept here as the reason for each change.

| Model | Change | Why |
|---|---|---|
| User | Add `termsAcceptedAt` (timestamp). Set at sign-up. Stored but never returned, like the password hash. `null` for seeded admins. | Record of consent (LOGIN-8) |
| User | Note on `fullName`: for `COMPANY` accounts it holds the company name at sign-up. | Company sign-up asks for no person's name |
| Company | Note on `verified`: `false` when created at sign-up | LOGIN-10 |
| New: CurrentUser | All User fields plus `company` (Company \| null, set when `role` is `COMPANY`) | Returned by log in, both register endpoints and `/auth/me`. Every logged-in nav uses it. |
| New, server-only: PasswordResetToken | `id`, `userId`, `tokenHash`, `expiresAt`, `usedAt` (timestamp \| null), `createdAt`. Never returned. | LOGIN-21. Needed for the ER diagram. |

Changes to the README conventions:

| Topic | Change |
|---|---|
| Status codes | Add `429` too many requests, with a `Retry-After` header, if LOGIN-23 is accepted |
| Status codes | `403` also means "account suspended" on log in (LOGIN-15). The list now says only "wrong role". |
| Errors | A `409` may also carry `errors`, so the page can show the message under a field |
| Error example | Its `instance` is `/api/v1/auth/register`, which this file splits in two. Change it to `/api/v1/auth/register/customer`. |

## Open questions

1. **Company sign-up details.** The mockup asks only for the company name, email and password. What does an admin check before verifying a company? If the answer is an ABN or Vietnamese tax code, phone, address or a contact person's name, add those fields to `register/company` and the Company model.
2. **Unverified companies.** What can a company do before an admin verifies it? Proposal: log in and add vehicles, but its vehicles don't appear in search until it is verified. This affects `search.md`.
3. **Where new customers land.** The mockup sends renters to My bookings after both log in and sign up. A new customer has no bookings. Should sign-up go to Search instead?
4. **Forgot and reset views.** The mockup has no screen to type an email for a reset, or to set a new password. Add `?view=forgot` and `?view=reset&token=…` to the log in mockup and wireframes. Also choose how email is sent: Spring Mail with SMTP is the simplest. In development, log the link instead of sending it.
5. **CSRF.** The README doesn't cover it, and Spring Security turns it on for session logins. Either (a) use `CookieCsrfTokenRepository.withHttpOnlyFalse()`, have the page send the `X-XSRF-TOKEN` header, and add `GET /api/v1/auth/csrf` (Public, `204`, sets `XSRF-TOKEN`) so the page can get a token before its first `POST`; or (b) turn CSRF off for `/api/**` and rely on `SameSite=Lax` cookies. Option (a) is safer.
6. **Nav booking count.** Resolved: the count stays out of `/me`. The nav reads `activeCount` from `GET /api/v1/bookings/summary` (search.md).
7. **Return to the previous page.** Should log in send the user back to where they were, for example a vehicle they tried to book while logged out (`?next=`)? The mockup doesn't show this.
8. **Throttling.** Do LOGIN-23 and LOGIN-24 go in the SRS (§3.2), and are the numbers right?
9. **Email verification.** New accounts can use the site straight away. Should they confirm their email first? It isn't in the mockup, so the proposal is no, at least for the MVP.
