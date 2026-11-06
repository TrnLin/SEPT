# API schema, by page

The REST API the backend needs so each mockup page can work. Each page has its own file. This file holds the rules every endpoint follows, the shared data models, an index of every endpoint, and the decisions the team still has to make.

Use these files to write SRS §2 (functional requirements), §2.8 (business rules), §3.2 (security) and §5 (UI design). Every endpoint names its SRS feature area, and every rule has an ID (`LP-`, `LOGIN-`, `SR-`, `VEH-`) that a requirement or acceptance test can cite.

> Draft. Nothing here is built yet. If the team changes an endpoint, update the page file and log the change in `../decisions/`.

## Pages

| Page | Mockup | Schema | Rules |
|---|---|---|---|
| Landing | `assets/mockups/landing-3d/` | [landing.md](landing.md) | LP-1 to LP-25 |
| Log in and sign up | `assets/mockups/login/` | [login.md](login.md) | LOGIN-1 to LOGIN-24 |
| Search (customer) | `assets/mockups/search/` | [search.md](search.md) | SR-1 to SR-24 |
| Vehicle detail (customer) | `assets/mockups/vehicle/` (not committed yet) | [vehicle.md](vehicle.md) | VEH-1 to VEH-35 |

The logo concept sheet (`assets/mockups/logo/`) has no data, so it has no schema.

Static pages with no API, linked from the landing page: `/for-companies`, `/terms` and `/privacy` ([landing.md](landing.md) LP-25). They have no mockup yet, and each needs a simple wireframe for SRS §5.

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
| `GET /api/v1/places` | Place suggestions for "Where" | 2.3 | Public | [search.md](search.md) |
| `GET /api/v1/places/{id}` | One place, from `placeId` | 2.3 | Public | [search.md](search.md) |
| `GET /api/v1/vehicles/search` | Search results for a place and dates | 2.3 | Public | [search.md](search.md) |
| `GET /api/v1/vehicles/search/facets` | Filter options with counts, empty-state suggestions | 2.3 | Public | [search.md](search.md) |
| `GET /api/v1/vehicles/compare` | Up to 3 vehicles side by side | 2.3 | Public | [search.md](search.md) |
| `GET /api/v1/bookings/summary` | Active booking count for the nav | 2.4 | `CUSTOMER` | [search.md](search.md) |
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
| 2.2 Vehicles | Company dashboard: add, edit and remove listings |
| 2.4 Bookings | My bookings (list, detail, cancel); company: approve or reject requests |
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
| Money | Amounts are decimals with 2 places (`BigDecimal` in Java), for example `68.00`. Every price is in AUD. A response that holds prices also has `"currency": "AUD"`. |
| Auth | Spring Security session. Log in sets an `HttpOnly` session cookie. "Keep me logged in" adds a remember-me cookie. Endpoints marked **Public** need no session. For `/api/**`, an unauthenticated call gets `401`, not a redirect to a login form. |
| CSRF | Proposal: keep Spring's CSRF protection with a readable `XSRF-TOKEN` cookie; the page sends it back in the `X-XSRF-TOKEN` header. See [login.md](login.md) open question 5. |
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
| `403` | Wrong role, or the account is suspended (log in) |
| `404` | Not found, or hidden from this caller (for example an unlisted vehicle) |
| `409` | Conflict: the email is taken, or the dates clash with a booking |
| `429` | Too many attempts, with a `Retry-After` header. Proposal: [login.md](login.md) LOGIN-23. |

## Theme: light and dark mode

Every page supports a light and a dark theme. It needs no API.

| Topic | Rule |
|---|---|
| Default | Follows the visitor's system setting (`prefers-color-scheme`). |
| Toggle | System, Light and Dark, in the header: next to **Log in** when logged out, next to the account menu when logged in (assumption). |
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
| `fullName` | string | For a `COMPANY` account, the company name given at sign-up |
| `email` | string | Unique, stored in lower case |
| `role` | enum | `CUSTOMER`, `COMPANY`, `ADMIN` |
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
| `name` | string | |
| `verified` | boolean | `false` when created at sign-up. Set by an admin. |
| `rating` | decimal \| null | _derived_: average review rating, 1 decimal place. `null` with no reviews. |
| `reviewCount` | int | _derived_ |
| `createdAt` | timestamp | "On RentXe since 2021" |
| `openingHours` | object[] | Display text, for example `{ "days": "Mon – Fri", "hours": "7:00 – 19:00" }`. Real times are needed if closed days block pick-ups ([vehicle.md](vehicle.md) open question 6). |

### Place

A point customers search from: a city, an area (suburb or district) or an airport. The team seeds them.

| Field | Type | Notes |
|---|---|---|
| `id` | long | |
| `name` | string | Short name for headings: `Melbourne CBD` |
| `label` | string | Full name for suggestions and the Where field: `Melbourne CBD, VIC` |
| `kind` | enum | `CITY`, `AREA`, `AIRPORT` |
| `city` | string | Same spelling as `Location.city`, so search can match it |
| `lat`, `lng` | decimal | The point distances are measured from |
| `timeZone` | string | IANA zone, for example `Australia/Melbourne` |
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

### Vehicle

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
| `startDate`, `endDate` | date | Pick-up and return dates |
| `status` | enum | `REQUESTED`, `APPROVED`, `REJECTED`, `CANCELLED`, `PICKED_UP`, `RETURNED` |
| `insurance` | enum | `BASIC` (default), `PREMIUM` |
| `pricePerDay` | decimal | The vehicle's daily rate when the request was saved |
| `insurancePerDay` | decimal | The cover's daily price then. `0.00` for `BASIC`. |
| `excess` | decimal | The chosen cover's excess then |
| `deposit` | decimal | The vehicle's deposit then |
| `totalPrice` | decimal | _derived_ once, when the request is saved, by the fee rule ([vehicle.md](vehicle.md) VEH-10 to VEH-15), then stored. A later price change does not change it. |
| `createdAt` | timestamp | |
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
| 1 | Does a `REQUESTED` booking hold its dates, or only an `APPROVED` one? If requests hold dates, when does an unanswered one expire? | `REQUESTED`, `APPROVED` and `PICKED_UP` block. No expiry yet, and no `EXPIRED` status. | SR-6, VEH-6, vehicle.md Q1 and Q2 |
| 2 | Can a rental start today? | No. The earliest pick-up is tomorrow, because the company must approve first. The landing review ("picked it up the same afternoon") and the vehicle calendar (lets you click today) need changing to match. | LP-3, SR-4, VEH-3 |
| 3 | Is the return day free for the next pick-up? | No. A booking blocks both its start and end days, as the vehicle mockup's calendar shows. | SR-7, VEH-6, VEH-7 |
| 4 | "Only 2 left": is one Vehicle row one physical vehicle? | Yes, so the label has nothing to count. search.md shows option A (`Vehicle.units`) because the mockup does; option B drops the label. | SR-8, search.md Q1, vehicle.md Q12 |
| 5 | Which companies appear in search? | Only `verified` ones. Company has no suspended status yet. | SR-2, login.md Q2, search.md Q5 |
| 6 | One rating per review, or one for the vehicle and one for the company? | Decided: one `rating` for the vehicle and the service together. The landing copy will be reworded. | landing.md Q3 |
| 7 | One cancellation rule for everyone, or one per company? | Decided: one rule for everyone. Free until 24 hours before pick-up, then 50% of `totalPrice`. The landing copy will be reworded. | VEH-22, VEH-23, landing.md Q4 |
| 8 | Can logged-out visitors use search and vehicle pages? | The read endpoints are Public; sending a booking needs a `CUSTOMER` login. No logged-out nav is mocked up. | search.md Q6, vehicle.md Q16 |
| 9 | Is payment in scope? | No. RentXe records amounts; the page says "You won't be charged until the company approves". | vehicle.md Q8 |
