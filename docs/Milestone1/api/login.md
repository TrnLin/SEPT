# Log in and sign up

One page to log in, sign up as a renter or a rental company, and ask for a password reset. Admins log in here too.

| | |
|---|---|
| Mockup | `assets/mockups/login/index.html` |
| SRS area | 2.1 User and Profile Management |
| Owns | Every endpoint under `/api/v1/auth/*` |
| Auth approach | **Not decided** (Q16). This file is written for option A, Spring Security sessions. Option B, Supabase Auth on the page, would change the cookies, log out, reset password and CSRF parts. |

## Page states

| URL | View | Account type | Title | Submit button |
|---|---|---|---|---|
| `login/` | Log in | Renter | Welcome back. | Log in |
| `login/?as=company` | Log in | Rental company | Back to your fleet. | Log in |
| `login/?view=signup` | Sign up | Renter | Start riding. | Create account |
| `login/?view=signup&as=company` | Sign up | Rental company | List your fleet. | Register company |

- Any other `view` value means log in. Any other `as` value means renter.
- Any state can also carry `next`, the page to return to after success, for example `login/?next=%2Fvehicles%2F68%3Fstart%3D2026-12-11%26end%3D2026-12-14` (LOGIN-29). Switching the view or account type keeps it.
- Switching the view or account type rewrites the URL without a reload.
- The landing page links to all four states. The customer nav's "Log out" link ends here too.
- Other states: field errors (shown on submit, then updated as the user types), a busy button ("Logging in…", "Creating account…"), and a toast.
- There is no admin tab. An admin can log in with either tab selected.

## What the page shows

| UI element | View | Source |
|---|---|---|
| Side panel statement and booking tracker | Both | Static copy that changes with the account type. No data. |
| Renter / Rental company toggle | Both | URL `as`. Sign up: picks the endpoint (`register/customer` or `register/company`). Log in: changes the copy only and sends nothing (LOGIN-13). |
| Full name | Sign up, renter | `fullName` on `POST /api/v1/auth/register/customer` |
| Company name, Your name, Phone | Sign up, company | `companyName`, `fullName` and `phone` on `POST /api/v1/auth/register/company`. The mockup has only Company name so far; Your name and Phone are to be added (Q1). |
| Email | Both | `email` on log in and both register endpoints |
| Password, Show / Hide | Both | `password`. Show / Hide is client-only. |
| "At least 8 characters." | Sign up | Static hint for LOGIN-5 |
| Keep me logged in (ticked by default) | Log in | `rememberMe` on `POST /api/v1/auth/login` |
| Forgot password? | Log in | `POST /api/v1/auth/forgot-password` with the Email field's value |
| I agree to the Terms and Privacy policy | Sign up | `acceptTerms` on both register endpoints |
| Terms, Privacy, Help links | Both | Static pages, no API. Terms and Privacy go to `/terms` and `/privacy` (landing LP-25); Help goes to `/help` (LOGIN-31). |
| "Admins log in here too." | Both | Static |
| Theme toggle (decided 2026-11-06, not in the mockup) | Both | Icon button at the right end of the top row, after the Sign up / Log in switch. It cycles System, Light and Dark and is saved in `localStorage` (README, Theme). No API. |
| After success | Both | Redirect by `role` in the response (table below) |
| Page load (decided 2026-11-06, not in the mockup) | Both | `GET /api/v1/auth/me`. `200`: already logged in, so the user is sent on as after a log in (LOGIN-30). `401`: show the form. |

Where server errors appear (decided 2026-11-06, LOGIN-32). Errors about one field go under that field; everything else goes in an error banner at the top of the form, under the heading. The mockup has the field slots but no banner yet:

| Server error | Shown |
|---|---|
| `errors[].field` is `fullName`, `companyName` or `phone` | Under that field |
| `errors[].field` is `email`, `password` or `acceptTerms` | Under that field or the checkbox |
| `401` from log in | Banner: `detail` ("Email or password is incorrect"). The email stays filled in; the password is cleared and gets the focus. |
| `403` from log in | Banner: `detail` ("This account is suspended. Contact RentXe support.") with a link to `/help` |
| `429` from log in | Banner: `detail` ("Too many attempts. Try again in 15 minutes."), the time taken from `Retry-After` |
| Network error or `5xx` | Banner: "Something went wrong. Try again." |

Where the user goes after log in or sign up. A customer with a valid `next` goes there instead (LOGIN-29):

| `role` | Goes to | Source |
|---|---|---|
| `CUSTOMER` | After sign-up: Search. After log in: My bookings when the customer has an active booking (`activeCount` > 0), otherwise Search (LOGIN-28). | Decided 2026-11-06 (Q3). The mockup's toast still says "this would open your bookings" for both. |
| `COMPANY` | Company dashboard | Mockup toast: "this would open the rental company dashboard" |
| `ADMIN` | Admin dashboard | Assumption. The mockup only says admins log in here. |

None of these pages has a mockup yet.

## Endpoints

Written for option A (Spring Security sessions). The auth approach is still open (Q16).

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

**Two register endpoints, not one with a role field.** The server sets the role from the path. A client can never ask for `ADMIN`, and there is no role value to validate or reject. Each request body is a plain DTO with Bean Validation annotations, so no field is "required only when role is X". Company sign-up has fields that customer sign-up doesn't (`companyName`, `phone`). The page already knows which one to call from the toggle.

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
| `companyName` | string | yes | Trimmed. 1 to 100 characters (LOGIN-7). Unique, ignoring case and extra spaces (LOGIN-11). |
| `fullName` | string | yes | The person registering the company. As for customer sign-up (LOGIN-7). |
| `phone` | string | yes | The company's contact number. 8 to 15 digits (LOGIN-25). Stored on the Company. |
| `email` | string | yes | As for customer sign-up |
| `password` | string | yes | As for customer sign-up |
| `acceptTerms` | boolean | yes | Must be `true` |

```http
POST /api/v1/auth/register/company
Content-Type: application/json

{
  "companyName": "Saigon Wheels Co.",
  "fullName": "Lan Nguyen",
  "phone": "0412 345 678",
  "email": "hello@saigonwheels.example",
  "password": "fleet-district1",
  "acceptTerms": true
}
```

`201 Created`

```json
{
  "id": 57,
  "fullName": "Lan Nguyen",
  "email": "hello@saigonwheels.example",
  "role": "COMPANY",
  "status": "ACTIVE",
  "companyId": 7,
  "createdAt": "2026-11-06T08:30:00Z",
  "company": {
    "id": 7,
    "name": "Saigon Wheels Co.",
    "phone": "0412345678",
    "verified": false,
    "rating": null,
    "reviewCount": 0
  }
}
```

**Cookies:** as for customer sign-up.

| Status | When |
|---|---|
| `400` | A field breaks a rule. One `errors` entry per field. |
| `409` | The email is used (`errors[].field` = `email`), or the company name is taken (`companyName`). Both are listed if both clash. |

Notes:
- Creates one User and one Company in one transaction (LOGIN-10). The Company starts with `verified: false`.
- `fullName` is the person who fills in the form, for example a manager. It goes on the User (the login), so the account menu shows a person: "LN · Lan · Company account". `companyName` and `phone` go on the Company.
- The admin sees the company name, the person's name and the phone number before verifying the company, and can phone them to check.
- One login per company. Separate logins for several staff are not in the MVP. The model allows it later, because each User points to its Company through `companyId`.

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

| Endpoint | Defined in | When |
|---|---|---|
| `GET /api/v1/bookings/summary` | [search.md](search.md) | Right after a `CUSTOMER` logs in, to choose between My bookings and Search (LOGIN-28). Not called after sign-up, or when a valid `next` is given. |

The pages users reach after log in (My bookings, Search, company dashboard, admin dashboard) load their own data.

The admin endpoints that verify a company and suspend an account belong to the admin page, which is not written yet. LOGIN-15 and LOGIN-16 say what a suspension does to log in. LOGIN-26 and LOGIN-27 say what verifying and rejecting a company do.

## Validation and business rules

The mockup gives only "required", the email format and "at least 8 characters". The other numbers here (maximum lengths, token lifetime, throttle limits) are proposals. The team can change them.

| # | Rule | SRS |
|---|---|---|
| LOGIN-1 | The server applies every rule below even when the page has already checked it. A sign-up sent straight to the API with a 7-character password gets `400`. | 2.1, 3.2 |
| LOGIN-2 | Email is trimmed and lower-cased before it is stored or looked up. After signing up as `Minh.Tran@example.com`, logging in as `minh.tran@example.com` succeeds. | 2.1 |
| LOGIN-3 | Email must match `^[^\s@]+@[^\s@]+\.[^\s@]+$` (the page's own check) and be at most 254 characters. Otherwise `400` on `email`. | 2.1 |
| LOGIN-4 | An email can belong to only one account, whatever the role. Signing up with a used email returns `409` on `email` and creates nothing. Each account has exactly one role, set at sign-up; no endpoint changes it. Someone who rents and also runs a company uses two accounts with two emails (decided 2026-11-06). | 2.1 |
| LOGIN-5 | A password set at sign-up or reset has 8 to 72 characters and at most 72 bytes in UTF-8 (the BCrypt limit). It is not trimmed. There are no other rules: no required upper case, digits or symbols, and no common-password list (decided 2026-11-06). A 7-character password gets `400` "must be at least 8 characters". | 2.1, 3.2 |
| LOGIN-6 | Passwords are stored only as BCrypt hashes. No response ever contains a password or a hash. | 3.2 |
| LOGIN-7 | Both sign-ups need `fullName`; company sign-up also needs `companyName`. Each is trimmed and must be 1 to 100 characters. A name of only spaces gets `400`. | 2.1 |
| LOGIN-8 | Sign-up needs `acceptTerms: true`. If it is `false` or missing, the response is `400` on `acceptTerms` and nothing is created. The time of acceptance is stored. | 2.1 |
| LOGIN-9 | Sign-up creates only `CUSTOMER` or `COMPANY` accounts, and the endpoint sets the role. No API request can create an `ADMIN`. In the MVP there is exactly one admin, seeded when the app starts: if no `ADMIN` account exists, Spring creates one from the settings `RENTXE_ADMIN_EMAIL`, `RENTXE_ADMIN_PASSWORD` and `RENTXE_ADMIN_NAME` (default "RentXe Admin"). The password must meet LOGIN-5. If an admin already exists, nothing changes, even if the settings do. If the settings are missing, no admin is created and a warning is logged. The password is never in the code or the repository; the dev and test profiles may seed a known admin for demos and tests, production never does. | 2.1, 3.2 |
| LOGIN-10 | Company sign-up creates one `ACTIVE` User with role `COMPANY` and one Company with `verified: false`, linked by `companyId`, in one transaction. If either fails, neither is saved. | 2.1, 2.8 |
| LOGIN-11 | Company names are unique. Two names clash if they match after trimming, turning runs of spaces into one, and ignoring case: registering "saigon  wheels co." when "Saigon Wheels Co." exists returns `409` on `companyName` with "A company with this name is already registered." The name is stored as typed (trimmed). Suspended companies keep their name, so it can't be reused to borrow their reviews. The same rule applies when a company renames itself later. The database enforces it with a unique index on the normalised name (decided 2026-11-06). | 2.1 |
| LOGIN-12 | A successful sign-up logs the new user in with a session cookie and no remember-me cookie. | 2.1 |
| LOGIN-13 | Log in ignores the Renter / Rental company toggle. The account's role decides where the user goes: `CUSTOMER` as in LOGIN-28, `COMPANY` to the company dashboard, `ADMIN` to the admin dashboard. A company logging in with "Renter" selected still reaches the company dashboard. | 2.1 |
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
| LOGIN-25 | Company sign-up needs `phone`. It may contain digits, spaces, brackets, dashes and a leading `+`. With those removed it must have 8 to 15 digits, otherwise `400` on `phone`. It is stored without spaces, brackets or dashes: `0412 345 678` is stored as `0412345678`. | 2.1 |
| LOGIN-26 | A company is **live** when its Company is `verified` and its account is `ACTIVE`. Only an admin can set `verified`. Before that, the company can log in, edit its profile and add vehicles, but its vehicles are not live: they are left out of search, return `404` from public vehicle endpoints (the company itself and admins can still read them) and cannot be requested. While `verified` is `false`, its dashboard says "Waiting for verification. Your vehicles go live once an admin approves you." Once an admin verifies it, all its listed vehicles go live with no further step. | 2.1, 2.8 |
| LOGIN-27 | There is no "rejected" state. To reject a company, an admin suspends its account. LOGIN-15 and LOGIN-16 then apply, and its vehicles leave search because the company is no longer live. The same happens when an admin suspends a company that is already verified. | 2.1, 2.8 |
| LOGIN-28 | Where a `CUSTOMER` goes after success. Sign-up: always Search. Log in: the page calls `GET /api/v1/bookings/summary`; with `activeCount` above 0 (a `REQUESTED`, `APPROVED` or `PICKED_UP` booking, SR-24) it goes to My bookings, and with 0 it goes to Search. A customer whose bookings are all returned or cancelled therefore lands on Search. If the summary call fails, it goes to Search. A valid `next` wins over both (LOGIN-29). | 2.1 |
| LOGIN-29 | Pages that send a logged-out user to log in add `next`, the path they were on, including its query: "Request to book" on the vehicle page, and any logged-in page whose API call returns `401` because the session ended. After a successful log in or sign-up, a `CUSTOMER` goes to `next` instead of the LOGIN-28 page; `COMPANY` and `ADMIN` ignore it and go to their dashboard. The same applies when an already logged-in customer opens the login page with `next`. `next` is used only if it is a path on our own site: it starts with one `/`, not `//` or `/\`, has no scheme or host, and is not the login page itself. Otherwise it is ignored and LOGIN-28 applies, with no error shown. Example: `next=https://evil.example` and `next=//evil.example` are ignored; `next=/vehicles/68?start=2026-12-11&end=2026-12-14` returns to that vehicle with the dates filled in. Returning never sends a booking request by itself; the customer clicks again. The check runs in the page; no endpoint takes `next`. | 2.1, 3.2 |
| LOGIN-30 | When the login page loads, it calls `GET /api/v1/auth/me` before showing the form. On `200` the user is already logged in: the page sends them where a fresh log in would (LOGIN-13, LOGIN-28, LOGIN-29) and never shows the form. On `401`, or if the call fails, it shows the form. Example: a logged-in customer with an approved booking who opens `/login` lands on My bookings; with `?next=/vehicles/68` they land on that vehicle. To switch accounts, a user logs out first from the account menu. | 2.1 |
| LOGIN-31 | Help links to `/help`, a static FAQ page with no API, for every visitor rather than for companies. Sections: **Your account** (signing up, forgot password, Keep me logged in, one role per email, so renting and running a company need two emails); **Renting** (request, the company approves, pick-up, return, review; the earliest pick-up is tomorrow; free cancellation until 24 h before pick-up, then 50%; RentXe takes no payment; bring your licence, the company checks it at pick-up); **Contact** (the support email from Contact us). Company questions get one line only: "Run a rental company? See how it works" linking to `/for-companies`. The answers must match the rules they describe, so update them when a rule changes. Needs a simple wireframe (decided 2026-11-06). | 5 |
| LOGIN-32 | Errors about one field (`400`, `409`) show under that field. Errors that aren't about one field (`401`, `403`, `429`, network errors and `5xx`) show in a single error banner at the top of the form, under the heading, with `role="alert"` so screen readers announce it. The banner stays until the user edits a field or submits again, and a new error replaces the old one. A `401` keeps the email, clears the password and moves the focus to it. Errors never use the toast; the toast is only for notices (decided 2026-11-06). | 3.3 |

## Changes to shared models

Merged into the README on 2026-11-06. Kept here as the reason for each change.

| Model | Change | Why |
|---|---|---|
| User | Add `termsAcceptedAt` (timestamp). Set at sign-up. Stored but never returned, like the password hash. `null` for seeded admins. | Record of consent (LOGIN-8) |
| User | Note on `fullName`: for `COMPANY` accounts it is the person who registered the company. | Q1: company sign-up asks for the person's name |
| Company | Add `phone` (string). Set at sign-up. Returned only to the company itself (in CurrentUser) and to admins, never in public responses such as search or the vehicle page. | Q1: the admin needs a way to contact the company before verifying it (LOGIN-25) |
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

1. **Company sign-up details.** Resolved 2026-11-06 ([decision](../decisions/company-signup-contact-person.md)): company sign-up also asks for the name of the person registering (`fullName`, on the User) and a phone number (`phone`, on the Company). The admin can phone them before verifying. ABN and business address are left out of sign-up; the company profile page can ask for them later. Mockup to-do: add "Your name" and "Phone" to the company sign-up form.
2. **Unverified companies.** Resolved 2026-11-06 ([decision](../decisions/unverified-company-setup-hidden.md)): an unverified company can log in, edit its profile and add vehicles, but nothing is public until an admin verifies it (LOGIN-26). An admin rejects a company by suspending its account; there is no "rejected" state (LOGIN-27). The admin page still needs a list of companies waiting for approval and a verify endpoint, and seed data should start the demo companies as verified.
3. **Where new customers land.** Resolved 2026-11-06 ([decision](../decisions/customer-landing-after-login.md)): sign-up goes to Search. Log in goes to My bookings only when the customer has an active booking, otherwise to Search (LOGIN-28). Mockup to-do: the toast after sign-up should say Search.
4. **Forgot and reset views.** The mockup has no screen to type an email for a reset, or to set a new password. Add `?view=forgot` and `?view=reset&token=…` to the log in mockup and wireframes. Also choose how email is sent: Spring Mail with SMTP is the simplest. In development, log the link instead of sending it.
5. **CSRF.** The README doesn't cover it, and Spring Security turns it on for session logins. Either (a) use `CookieCsrfTokenRepository.withHttpOnlyFalse()`, have the page send the `X-XSRF-TOKEN` header, and add `GET /api/v1/auth/csrf` (Public, `204`, sets `XSRF-TOKEN`) so the page can get a token before its first `POST`; or (b) turn CSRF off for `/api/**` and rely on `SameSite=Lax` cookies. Option (a) is safer.
6. **Nav booking count.** Resolved: the count stays out of `/me`. The nav reads `activeCount` from `GET /api/v1/bookings/summary` (search.md).
7. **Return to the previous page.** Resolved 2026-11-06 ([decision](../decisions/return-to-page-after-login.md)): yes, with `?next=` (LOGIN-29). Customers only, after log in and sign-up, and only to a page on our own site.
8. **Throttling.** Do LOGIN-23 and LOGIN-24 go in the SRS (§3.2), and are the numbers right?
9. **Email verification.** New accounts can use the site straight away. Should they confirm their email first? It isn't in the mockup, so the proposal is no, at least for the MVP.
10. **Admin accounts.** Resolved 2026-11-06 ([decision](../decisions/one-seeded-admin.md)): one admin, seeded at start-up from settings (LOGIN-9). Later, not in the MVP: the seeded admin can make other accounts admins. That feature has its own questions, listed in the decision file.
11. **Several roles on one account.** Resolved 2026-11-06 ([decision](../decisions/one-role-per-account.md)): no, one role per account (LOGIN-4). A customer who also runs a company uses two accounts. Customer and company on one account, with a view switcher, is a possible later feature; admin always stays a separate account.
12. **Unique company names.** Resolved 2026-11-06 ([decision](../decisions/unique-company-names.md)): yes, ignoring case and extra spaces, including suspended companies and later renames (LOGIN-11).
13. **Theme toggle and dark styles.** Resolved 2026-11-06 ([decision](../decisions/light-dark-theme.md)): the toggle goes at the right end of the top row, the same top-right spot as on other pages; on small screens it stays there after the logo and Back to home. Mockup to-do, dark styles: the side panel uses `--theme-band` with a `--theme-line` edge; the form, inputs and muted text use the `--theme-*` colours; the selected Renter / Company button turns white with black text; the orange submit button and the logo don't change.
14. **Help link.** Resolved 2026-11-06 ([decision](../decisions/static-help-page.md)): a static `/help` FAQ page for every visitor, about accounts and renting, with one line pointing companies to `/for-companies` (LOGIN-31). Mockup to-do: point Help at `/help` and add a wireframe for the page.
15. **Where server errors show.** Resolved 2026-11-06 ([decision](../decisions/form-error-banner.md)): field errors under the field; `401`, `403`, `429`, network errors and `5xx` in an error banner at the top of the form (LOGIN-32). Mockup to-do: add the banner, and stop using the toast for errors.
16. **Auth approach: open, not decided.** Kept open on 2026-11-06 for the team to choose ([options](../decisions/login-auth-approach.md), [diagram](../architecture/auth-flows.html), [PNG](../architecture/auth-flows-a-vs-b.png)). Both options keep Supabase as the Postgres database. **A, Spring Security sessions (recommended):** Spring checks the password (BCrypt, our `users` table) and keeps a server session; the browser holds only an `HttpOnly` `JSESSIONID` cookie, plus remember-me. This file is written for A. **B, Supabase Auth on the page:** the page signs up and logs in with Supabase's JavaScript library; Spring checks the Supabase JWT on each request against Supabase's public keys. Q4 (reset emails), Q5 (CSRF), Q8 (throttling), Q9 (email confirmation) and session length (LOGIN-17) wait on this choice.
