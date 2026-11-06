# API schema, by page

The REST API the backend needs so each mockup page can work. Each page has its own file. This file holds the rules every endpoint follows, the shared data models, an index of every endpoint, and the decisions the team still has to make.

Use these files to write SRS §2 (functional requirements), §2.8 (business rules), §3.2 (security) and §5 (UI design). Every endpoint names its SRS feature area, and every rule has an ID (`LP-`, `LOGIN-`, `SR-`, `VEH-`) that a requirement or acceptance test can cite.

> Draft. Nothing here is built yet. If the team changes an endpoint, update the page file and log the change in `../decisions/`.

## Pages

| Page | Mockup | Schema | Rules |
|---|---|---|---|
| Landing | `assets/mockups/landing-3d/` | [landing.md](landing.md) | LP-1 to LP-25 |
| Log in and sign up | `assets/mockups/login/` | [login.md](login.md) | LOGIN-1 to LOGIN-36 |
| Search (customer) | `assets/mockups/search/` | [search.md](search.md) | SR-1 to SR-29 |
| Vehicle detail (customer) | `assets/mockups/vehicle/` (not committed yet) | [vehicle.md](vehicle.md) | VEH-1 to VEH-41 |

The logo concept sheet (`assets/mockups/logo/`) has no data, so it has no schema.

Static pages with no API: `/for-companies`, `/terms` and `/privacy`, linked from the landing page ([landing.md](landing.md) LP-25), and `/help`, linked from the login page ([login.md](login.md) LOGIN-31). They have no mockup yet, and each needs a simple wireframe for SRS §5.

## Endpoint index

| Method and path | What it does | SRS | Access | Defined in |
|---|---|---|---|---|
| `POST /api/v1/auth/register/customer` | Sign up as a renter | 2.1 | Public | [login.md](login.md) |
| `POST /api/v1/auth/register/company` | Sign up as a rental company. Also creates the Company, unverified | 2.1 | Public | [login.md](login.md) |
| `POST /api/v1/auth/login` | Log in | 2.1 | Public | [login.md](login.md) |
| `POST /api/v1/auth/logout` | Log out | 2.1 | Public | [login.md](login.md) |
| `GET /api/v1/auth/me` | The logged-in user, for every nav | 2.1 | Any role | [login.md](login.md) |
| `POST /api/v1/auth/forgot-password` | Email a reset link | 2.1 | Public | [login.md](login.md) |
| `POST /api/v1/auth/reset-password` | Set a new password from the link | 2.1 | Public | [login.md](login.md) |
| `GET /api/v1/auth/csrf` | Get a CSRF token cookie before the first `POST` | 3.2 | Public | [login.md](login.md) |
| `GET /api/v1/places` | Place suggestions for "Where" | 2.3 | Public | [search.md](search.md) |
| `GET /api/v1/places/{id}` | One place, from `placeId` | 2.3 | Public | [search.md](search.md) |
| `GET /api/v1/vehicles/search` | Search results for a place and dates | 2.3 | Public | [search.md](search.md) |
| `GET /api/v1/vehicles/search/facets` | Filter options with counts, empty-state suggestions | 2.3 | Public | [search.md](search.md) |
| `GET /api/v1/vehicles/compare` | Up to 3 vehicles side by side | 2.3 | Public | [search.md](search.md) |
| `GET /api/v1/exchange-rates` | The day's AUD rates, for showing prices in the city's currency | 2.3 | Public | [search.md](search.md) |
| `GET /api/v1/bookings/summary` | Active booking count for the nav, and where a customer goes after log in (login.md LOGIN-28) | 2.4 | `CUSTOMER` | [search.md](search.md) |
| `GET /api/v1/vehicles/{id}` | One vehicle, with its company and review summary | 2.2 | Public | [vehicle.md](vehicle.md) |
| `GET /api/v1/vehicles/{id}/availability` | Booked days for the calendar | 2.2 | Public | [vehicle.md](vehicle.md) |
| `GET /api/v1/vehicles/{id}/quote` | Price for chosen dates and cover | 2.4 | Public | [vehicle.md](vehicle.md) |
| `POST /api/v1/bookings` | Send a booking request | 2.4 | `CUSTOMER` | [vehicle.md](vehicle.md) |
| `GET /api/v1/vehicles/{id}/reviews` | Reviews of one vehicle | 2.6 | Public | [vehicle.md](vehicle.md) |
| `GET /api/v1/vehicles/{id}/similar` | Up to 3 similar vehicles | 2.3 | Public | [vehicle.md](vehicle.md) |

The landing page's reviews are static sample content, so it has no endpoint of its own. `GET /api/v1/reviews/featured` is kept in [landing.md](landing.md) as an option for later, not in the MVP.

### Not covered yet

These parts of the brief have no mockup, so they have no endpoints here. Add a page file when the mockup exists.

| Area | Pages still to mock up |
|---|---|
| 2.1 Accounts | Customer profile, company profile, admin user and company management |
| 2.2 Vehicles | Company dashboard: add, edit and remove listings. The vehicle form (assumed at `/company/vehicles/{id}/edit`) is also opened from **Edit** on search and the vehicle page, and returns to `next` after saving (search.md SR-26, vehicle.md VEH-40) |
| 2.3 Search and comparison | The compare page (`/compare?ids=…`), opened from the search page's compare tray. Its endpoint is ready in [search.md](search.md) (endpoint 3, SR-20) |
| 2.4 Bookings | My bookings (list, detail, cancel, extend: VEH-38); company: approve or reject requests and extensions |
| 2.5 Pick-up and return | Company: record pick-up, return, condition and the final fee |
| 2.6 Reviews | Write a review after a returned booking; company page with its reviews |

## Conventions

| Topic | Rule |
|---|---|
| Base path | `/api/v1` |
| Format | JSON, UTF-8. Field names in `camelCase`. Enum values in `UPPER_SNAKE_CASE`. |
| IDs | Numeric `long`, the JPA default. Sent as JSON numbers. |
| Dates | Rental dates are ISO dates with no time: `2026-12-11`. Timestamps are ISO 8601 in UTC: `2026-11-06T08:30:00Z`. |
| Rental dates in the API | Query parameters and bodies call them `startDate` and `endDate`, like Booking. Page URLs keep the mockups' `from` and `to`. |
| "Today" | The date in the pick-up place's time zone (`Location.timeZone`), or the searched place's (`Place.timeZone`) when there is no single vehicle. |
| Searched place | Travels between pages and to the API as `placeId`. The server works out distances from it. |
| Money | Amounts are decimals with 2 places (`BigDecimal` in Java), for example `68.00`. Every price is stored, worked out and returned in AUD. A response that holds prices also has `"currency": "AUD"`. Pages show amounts in the city's currency (`Place.currency`), converted with a daily rate ([search.md](search.md) SR-28); a booking keeps the rate it was sent with (VEH-41). |
| Auth | Spring Security session (team decision 10). Supabase is only the database. Log in sets an `HttpOnly` session cookie. "Keep me logged in" adds a remember-me cookie. Endpoints marked **Public** need no session. For `/api/**`, an unauthenticated call gets `401`, not a redirect to a login form. |
| CSRF | Spring's CSRF protection stays on. A readable `XSRF-TOKEN` cookie; the shared `api()` wrapper sends it back in the `X-XSRF-TOKEN` header on every `POST`, `PATCH`, `PUT` and `DELETE`. Missing or wrong: `403` ([login.md](login.md) LOGIN-36). |
| Origin | The pages and the API share one origin, so cookies work without CORS: Spring serves the pages, or a frontend dev server proxies `/api` to Spring. |
| Roles | `CUSTOMER`, `COMPANY`, `ADMIN`. An endpoint lists the roles allowed to call it. |
| Lists | Spring Data paging: `?page=0&size=20&sort=price,asc`. The response is `{ "content": [...], "page": { "size", "number", "totalElements", "totalPages" } }`. |
| Errors | RFC 7807 problem details (Spring's `ProblemDetail`), content type `application/problem+json`. Validation errors, and a `409` tied to a field, add an `errors` array of `{ "field", "message" }`. |

Error example:

```json
{
  "type": "about:blank",
  "title": "Bad Request",
  "status": 400,
  "detail": "Validation failed",
  "instance": "/api/v1/auth/register/customer",
  "errors": [{ "field": "password", "message": "must be at least 8 characters" }]
}
```

Status codes used:

| Code | Meaning |
|---|---|
| `200` | OK |
| `201` | Created. The `Location` header points to the new resource. |
| `204` | Done, no body |
| `400` | Validation failed |
| `401` | Not logged in, or wrong email or password |
| `403` | Wrong role, the account is suspended (log in), or the CSRF token is missing or wrong on a `POST`, `PATCH`, `PUT` or `DELETE` ([login.md](login.md) LOGIN-36) |
| `404` | Not found, or hidden from this caller (for example an unlisted vehicle) |
| `409` | Conflict: the email is taken, or the dates clash with a booking |
| `429` | Too many failed log ins, with a `Retry-After` header ([login.md](login.md) LOGIN-23) |

## Theme: light and dark mode

Every page supports a light and a dark theme. It needs no API.

| Topic | Rule |
|---|---|
| Default | Follows the visitor's system setting (`prefers-color-scheme`). |
| Toggle | System, Light and Dark, at the top right of every page: next to **Log in** when logged out, next to the account menu when logged in. The login page has neither, so it sits at the right end of its top row ([login.md](login.md) Q13). |
| Saved | In the browser's `localStorage`, key `rentxe-theme`, value `system`, `light` or `dark`. It holds on every page and after a reload, but not across browsers or devices. No User field, no endpoint. |
| First paint | A small script in `<head>` reads the saved value before the page draws, so the page never flashes the wrong theme. |
| Not themed | The landing page's 3D hero scene. Its sky follows the visitor's clock ([landing.md](landing.md) LP-19, LP-22). |
| Design | `assets/mockups/shared/tokens.css` has the theme colours (`--theme-bg`, `--theme-text`, `--theme-muted`, `--theme-line`, `--theme-fill`, `--theme-card`, `--theme-band`), light by default and dark under `data-theme="dark"`. Same palette: black background, white text, the same orange. The landing mockup uses them; login, search and vehicle still use fixed light colours and need the same pass. |
| SRS | Usability requirement for §3.3, for example: every page is readable in both themes, with text contrast of at least 4.5:1. |

## Shared models

The page files use these models and do not redefine them. Fields marked _derived_ are worked out by the server and never sent by the client. Fields marked _server only_ are stored but never returned.

### User

| Field | Type | Notes |
|---|---|---|
| `id` | long | |
| `fullName` | string | For a `COMPANY` account, the person who registered the company |
| `email` | string | Unique, stored in lower case |
| `role` | enum | `CUSTOMER`, `COMPANY`, `ADMIN`. One role per account, set at sign-up (LOGIN-4). |
| `status` | enum | `ACTIVE`, `SUSPENDED`. Admins can suspend accounts. |
| `companyId` | long \| null | Set when `role` is `COMPANY` |
| `createdAt` | timestamp | |
| `passwordHash` | string | _server only_ |
| `termsAcceptedAt` | timestamp \| null | _server only_. Set at sign-up. `null` for seeded admins. |

### CurrentUser

What log in, both sign-ups and `GET /api/v1/auth/me` return: every User field that is returned, plus `company` (Company, or `null` unless `role` is `COMPANY`). The nav works out the first name, initials and account label from it ([login.md](login.md)).

### PasswordResetToken

_server only_. `id`, `userId`, `tokenHash`, `expiresAt`, `usedAt` (timestamp \| null), `createdAt`. Rules in [login.md](login.md) (LOGIN-21).

### Company

| Field | Type | Notes |
|---|---|---|
| `id` | long | |
| `name` | string | Unique, ignoring case and extra spaces (login.md LOGIN-11) |
| `phone` | string | Contact number from sign-up, digits only (LOGIN-25). Returned only to the company itself and to admins, never in public responses. |
| `verified` | boolean | `false` when created at sign-up. Set by an admin. The company is live (its vehicles are public) only when `verified` and its account is `ACTIVE` (login.md LOGIN-26). |
| `rating` | decimal \| null | _derived_: average review rating, 1 decimal place. `null` with no reviews. |
| `reviewCount` | int | _derived_ |
| `createdAt` | timestamp | "On RentXe since 2021" |
| `openingHours` | object[] | Display text, for example `{ "days": "Mon – Fri", "hours": "7:00 – 19:00" }`. Real times are needed if closed days block pick-ups ([vehicle.md](vehicle.md) open question 6). |

### Place

A point customers search from: a city, an area (suburb or district) or an airport. The team seeds them: customers pick from this fixed list, with no outside geocoder ([decision](../decisions/fixed-place-list.md)). Open search through a geocoder is noted as a later option in [search.md](search.md) Q7.

| Field | Type | Notes |
|---|---|---|
| `id` | long | |
| `name` | string | Short name for headings: `Melbourne CBD` |
| `label` | string | Full name for suggestions and the Where field: `Melbourne CBD, VIC` |
| `kind` | enum | `CITY`, `AREA`, `AIRPORT` |
| `city` | string | Same spelling as `Location.city`, so search can match it |
| `lat`, `lng` | decimal | The point distances are measured from |
| `timeZone` | string | IANA zone, for example `Australia/Melbourne` |
| `currency` | string | The city's display currency, `AUD` or `VND`. Every place carries its city's. Prices are still stored in AUD (SR-28). |
| `otherNames` | string[] | _server only_. Matched by suggestions, for example `Saigon`, `HCMC` |

### Location

A vehicle's pick-up and return point.

| Field | Type | Notes |
|---|---|---|
| `area` | string | Suburb or district shown to customers, for example `Carlton`, `District 1` |
| `city` | string | Chosen from the `CITY` places, never typed, so search can match it |
| `address` | string | Pick-up address |
| `directions` | string \| null | How to find the desk, for example `Front desk, ground floor` |
| `lat`, `lng` | decimal | For distance and the map |
| `timeZone` | string | IANA zone, for example `Asia/Ho_Chi_Minh`. Decides "today" and the 10:00 pick-up time. |
| `currency` | string | _derived_ from the `CITY` place for `city`: the display currency, `AUD` or `VND` ([search.md](search.md) SR-28). Not stored. |

### Vehicle

One Vehicle is one physical vehicle, with one plate. A company with three identical cars lists three (team decision 4).

| Field | Type | Notes |
|---|---|---|
| `id` | long | |
| `companyId` | long | Owner |
| `type` | enum | `CAR`, `MOTORBIKE` |
| `brand` | string | For example `Toyota` |
| `model` | string | For example `Corolla Hybrid` |
| `year` | int | |
| `bodyStyle` | enum | Cars: `SEDAN`, `HATCHBACK`, `SUV`, `PEOPLE_MOVER`. Motorbikes: `SCOOTER`, `MANUAL_BIKE`. |
| `transmission` | enum | `AUTOMATIC`, `MANUAL` |
| `seats` | int | |
| `engineCc` | int \| null | Motorbikes only |
| `fuel` | enum \| null | `PETROL`, `DIESEL`, `HYBRID`, `ELECTRIC` |
| `fuelDetail` | string \| null | Consumption or range, for example `4.4 L / 100 km`, `510 km range` |
| `bags` | int \| null | Cars: large bags that fit |
| `helmets` | int \| null | Motorbikes: helmets supplied |
| `features` | string[] | Other short extras, for example `"Top box"`, `"Raincoats"` |
| `plateNumber` | string | For example `1XR·4KD`, `59-X1 234.56` |
| `plateRegion` | string | State or country that issued the plate, for example `VIC`, `VN` |
| `odometerKm` | int | Reading at the last return. Updated by the return flow (§2.5). |
| `minimumAge` | int | Youngest allowed driver or rider |
| `pricePerDay` | decimal | AUD |
| `deposit` | decimal | Refundable, held at pick-up, not part of a booking's `totalPrice` |
| `insuranceOptions` | InsuranceOption[] | Exactly one `BASIC` and one `PREMIUM` |
| `location` | Location | Pick-up and return point |
| `imageUrls` | string[] | Empty: the page draws a silhouette for the `type` |
| `listed` | boolean | `false` hides it from customers without deleting it |

InsuranceOption:

| Field | Type | Notes |
|---|---|---|
| `cover` | enum | `BASIC`, `PREMIUM` |
| `pricePerDay` | decimal | Always `0.00` for `BASIC` |
| `excess` | decimal | The most the customer pays towards damage |

### Booking

| Field | Type | Notes |
|---|---|---|
| `id` | long | |
| `vehicleId` | long | |
| `customerId` | long | |
| `companyId` | long | _derived_ from the vehicle |
| `startDate`, `endDate` | date | Pick-up and return dates. At most 30 days apart when booked (VEH-37). `endDate` moves later when an extension is approved (VEH-38). |
| `status` | enum | `REQUESTED`, `APPROVED`, `REJECTED`, `CANCELLED`, `EXPIRED`, `PICKED_UP`, `RETURNED`. `EXPIRED`: the company did not answer in time ([vehicle.md](vehicle.md) VEH-36). |
| `insurance` | enum | `BASIC` (default), `PREMIUM` |
| `pricePerDay` | decimal | The vehicle's daily rate when the request was saved |
| `insurancePerDay` | decimal | The cover's daily price then. `0.00` for `BASIC`. |
| `excess` | decimal | The chosen cover's excess then |
| `deposit` | decimal | The vehicle's deposit then |
| `totalPrice` | decimal | _derived_ once, when the request is saved, by the fee rule ([vehicle.md](vehicle.md) VEH-10 to VEH-15), then stored. A later price change does not change it. |
| `createdAt` | timestamp | |
| `respondedAt` | timestamp \| null | When the company approved or rejected |
| `displayCurrency`, `exchangeRate` | string, decimal | _derived_ when the request is saved: the currency shown for the vehicle's city and the day's AUD rate for it (`AUD`, `1.0` in Melbourne). Amounts on record stay AUD (VEH-41). |
| `expiresAt` | timestamp | _derived_ when the request is saved: 24 hours after `createdAt`, or 00:00 on the pick-up day in the pick-up place's time zone if sooner (VEH-36) |

### BookingExtension

A customer's request to keep a `PICKED_UP` booking longer ([vehicle.md](vehicle.md) VEH-38). Its endpoints come with the My bookings page.

| Field | Type | Notes |
|---|---|---|
| `id` | long | |
| `bookingId` | long | |
| `fromEndDate` | date | The booking's `endDate` when asked |
| `toEndDate` | date | The new return date: 1 to 30 days after `fromEndDate` |
| `status` | enum | `REQUESTED`, `APPROVED`, `REJECTED`, `CANCELLED` (withdrawn by the customer), `EXPIRED` |
| `amount` | decimal | _derived_ when saved: extra days × the booking's `pricePerDay` + `insurancePerDay`. Added to the booking's `totalPrice` on approval. |
| `createdAt` | timestamp | |
| `expiresAt` | timestamp | _derived_: 24 hours after `createdAt`, or 00:00 on `fromEndDate` if sooner |
| `respondedAt` | timestamp \| null | When the company approved or rejected |

### Review

| Field | Type | Notes |
|---|---|---|
| `id` | long | |
| `bookingId` | long | One review per `RETURNED` booking |
| `authorId` | long | The customer |
| `vehicleId`, `companyId` | long | _derived_ from the booking |
| `rating` | int | 1 to 5. One score for the whole rental: the vehicle and the service together. It counts toward the vehicle's average and the company's `rating`. |
| `comment` | string | |
| `createdAt` | timestamp | |

### Shapes shared between pages

| Shape | Defined in | Also used by |
|---|---|---|
| SearchResult (one result card) | [search.md](search.md) | Compare (search.md), similar vehicles (vehicle.md) |
| Availability (on a card) | [search.md](search.md) | Similar vehicles (vehicle.md) |

## Decisions for the team

The four files agree on each default below. Change one, and change every rule it lists. Record the outcome in `../decisions/`, one file per decision.

| # | Question | Current default | Rules affected |
|---|---|---|---|
| 1 | Does a `REQUESTED` booking hold its dates, or only an `APPROVED` one? If requests hold dates, when does an unanswered one expire? | Decided: `REQUESTED`, `APPROVED` and `PICKED_UP` block. A request the company has not answered within 24 hours, or by the start of the pick-up day if sooner, becomes `EXPIRED` and frees its dates. | SR-6, VEH-6, VEH-36, vehicle.md Q1 and Q2 |
| 2 | Can a rental start today? | No. The earliest pick-up is tomorrow, because the company must approve first. The landing review ("picked it up the same afternoon") and the vehicle calendar (lets you click today) need changing to match. | LP-3, SR-4, VEH-3 |
| 3 | Is the return day free for the next pick-up? | Decided: no. A booking blocks both its start and end days, as the vehicle mockup's calendar shows, leaving the return day for cleaning and late returns. | SR-7, VEH-6, VEH-7 |
| 4 | "Only 2 left": is one Vehicle row one physical vehicle? | Decided: yes. No `Vehicle.units`; a company with several identical vehicles lists each one. The "Only N left" label is dropped, so a vehicle is free or booked for the dates. | SR-8, search.md Q1, vehicle.md Q12 |
| 5 | Which companies appear in search? | Decided: only live companies, meaning `verified` by an admin with an `ACTIVE` account. Unverified companies can set up their profile and vehicles while hidden. An admin rejects or removes a company by suspending its account, so Company has no status of its own. | SR-2, VEH-35, LOGIN-26, LOGIN-27, login.md Q2, search.md Q5 |
| 6 | One rating per review, or one for the vehicle and one for the company? | Decided: one `rating` for the vehicle and the service together. The landing copy will be reworded. | landing.md Q3 |
| 7 | One cancellation rule for everyone, or one per company? | Decided: one rule for everyone. Free until 24 hours before pick-up, then 50% of `totalPrice`. The landing copy will be reworded. | VEH-22, VEH-23, landing.md Q4 |
| 8 | Can logged-out visitors use search and vehicle pages? | Decided: yes. Both pages work logged out, with the landing page's logged-out nav. Only **Request to book** needs a `CUSTOMER` login: a logged-out visitor goes to log in and comes back to the same vehicle and dates. | SR-25, VEH-39, LOGIN-29, search.md Q6, vehicle.md Q16 |
| 9 | Is payment in scope? | No. RentXe records amounts; the page says "You won't be charged until the company approves". | vehicle.md Q8 |
| 10 | How does login work? | Decided: option A, Spring Security sessions with an `HttpOnly` cookie and remember-me. Supabase is only the Postgres database; its Auth feature is not used. See [the decision](../decisions/login-auth-approach.md) and [the diagram](../architecture/auth-flows.html). | Every `/auth/*` endpoint, LOGIN-12 and LOGIN-15 to LOGIN-24, login.md Q4, Q5, Q8, Q9, Q16 |
| 11 | How long can a rental be, and how far ahead? | Decided: at most 30 days, starting at most 12 months ahead. A customer extends a running rental by up to 30 days at a time, from the last week before return, with the company's approval. | VEH-37, VEH-38, SR-4, vehicle.md Q5 |
| 12 | Which currency do pages show? | Decided: the city's. Amounts are stored and returned in AUD; pages show A$ in Melbourne and ₫ in Ho Chi Minh City, converted with a daily rate from ExchangeRate-API. A booking stores the currency and rate it was sent with. | SR-28, VEH-41, search.md Q14 |
