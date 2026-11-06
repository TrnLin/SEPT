# Vehicle detail (customer)

One vehicle in full: photos, specs, availability, pick-up place, company and reviews, plus the booking panel that sends a request.

Conventions and shared models: [README.md](README.md). This file only defines what is specific to this page.

| | |
|---|---|
| Mockup | `assets/mockups/vehicle/index.html`, screenshots in `assets/mockups/vehicle/screenshots/`. **Not committed yet.** |
| Who | A logged-in customer (the customer nav). The read endpoints are public, so a shared link also works. |
| Reached from | A search result or a similar-vehicle card, with the chosen dates in the link |

### URL parameters

| Parameter | Example | Meaning |
|---|---|---|
| `id` | `id=1` | Vehicle id. The mockup uses `mel-01`; real ids are numbers. |
| `placeId` | `placeId=2` | The place the customer searched (search.md). Sets the distance and the "Your search" marker. Missing: both are hidden. |
| `from`, `to` | `from=2026-12-11&to=2026-12-14` | Pick-up and return dates from the search page. When the customer changes dates, the page writes them back to the URL, so a reload or a shared link keeps them. Missing or invalid dates: the page picks defaults (the mockup uses a fixed 11–14 Dec; assumption: tomorrow, for 3 days). |
| `state=unavailable` | | Prototype only. Fakes another customer's booking over the dates. In the app this state comes from the quote (`available: false`) or a `409` from `POST /api/v1/bookings`. |
| `sheet=open` | | Prototype only. Opens the phone booking sheet on load (under 960 px). |

### States

| State | When | The booking panel shows |
|---|---|---|
| Free | Quote returns `available: true` | Insurance choice, price lines, deposit, **Request to book** |
| Picking | The customer clicked a pick-up day on the calendar and has not picked a return day yet | "Pick a return day", price lines show "—", button disabled. No quote call. |
| Clash | Some days in the range are booked | "Booked 11–12 Dec", "Not available for these dates", the next free dates, **Switch to 13–16 Dec**, "See similar vehicles" |
| Unavailable | Every day in the range is booked, for example another customer's request got in first | "Booked for your dates", "This car was booked by someone else for 11–14 Dec", the next free dates |
| Phone sheet | Screen under 960 px | The panel becomes a bottom sheet behind a bar with the total and **Request to book** (or **See options** when not free) |

### Calls

Numbers refer to the endpoints below.

| When | Calls |
|---|---|
| Page load | 1 detail, 2 availability (the two months shown), 3 quote, 5 reviews (first 6), 6 similar. Plus the nav calls from other pages. |
| Calendar arrows | 2 availability for the new months |
| Dates change | 3 quote, 6 similar |
| Insurance changes | 3 quote |
| Request to book | 4 booking request |

## What the page shows

"Static" means fixed text or a client-side rule, with no data from the API.

| Section | UI element | Source |
|---|---|---|
| Nav | First name "Minh", initials "MT", full name and email in the menu | `GET /api/v1/auth/me` (login.md) |
| Nav | "My bookings 02" | Active-booking count (search.md) |
| (01) Title | "Back to results · 11–14 Dec" | Static: a link to the search page with the current dates |
| (01) Title | "Search / Melbourne CBD / Listing MEL-01" | Searched place name from the link (static), then `id` |
| (01) Title | "Sedan · 2023 · Car" | 1 `bodyStyle`, `fuel` (only "Electric" is shown), `year`, `type` |
| (01) Title | "Toyota Corolla Hybrid." | 1 `brand`, `model` |
| (01) Title | Plate "1XR·4KD" with "VIC" tag | 1 `plateNumber`, `plateRegion` |
| (01) Title | "★ 4.7 · 50 reviews" | 1 `reviewSummary.average`, `reviewSummary.count` |
| (01) Title | "Yarra Car Co. · Melbourne CBD" | 1 `company.name`, `location.area` |
| Gallery | Main view and four thumbnails | 1 `imageUrls`. Empty list: the flat drawing for `type` and `bodyStyle` (static) |
| (02) Specs | Transmission | 1 `transmission`. The manual-licence note is static. |
| (02) Specs | Seats (car) or Engine (motorbike) | 1 `seats`, `engineCc`. Sub-notes ("Two rows", "rider and one passenger") are static. |
| (02) Specs | Fuel, or Range for electric | 1 `fuel`, `fuelDetail`. "Return it full" / "80% charge" is static by `fuel`. |
| (02) Specs | Luggage (car) or Helmets (motorbike) | 1 `bags` or `helmets`. "Fits 3 carry-ons" is static. |
| (02) Specs | Minimum age | 1 `minimumAge`. Sub-note static. |
| (02) Specs | Licence | Static, from `type` |
| (02) Specs | Odometer "18,420 km" | 1 `odometerKm` |
| (02) Specs | Year, "Listed as MEL-01 · plate 1XR·4KD" | 1 `year`, `id`, `plateNumber` |
| (02) Specs | "From Yarra Car Co.'s listing …" | 1 `company.name` |
| (03) Availability | Booked days (hatched), "4 days booked" / "All free" per month | 2 `bookedDates`. The page counts them per month. |
| (03) Availability | Today marker, past days greyed | 2 `today` |
| (03) Availability | Month arrows | Static: two months at a time, from this month to the 11th month ahead (Nov 2026 to Oct 2027 in the mockup) |
| (03) Availability | Your dates, clash days in red | URL dates; 3 `bookedDates` |
| (03) Availability | Clash message, "Use 13–16 Dec" | 3 `bookedDates`, `nextAvailable` |
| (03) Availability | "Fri 11 Dec → Mon 14 Dec · 3 days · A$204" | 3 `days`, `totalPrice` |
| (04) Pick-up | "0.8 km from Melbourne CBD, where you searched" | 1 `distanceKm`; place name from `GET /api/v1/places/{id}` (search.md) |
| (04) Pick-up | Map with pick-up pin and "Your search" | 1 `location.lat`, `location.lng`; the searched place's `lat`, `lng` |
| (04) Pick-up | "212 Flinders Lane", "Melbourne VIC 3000 · front desk, ground floor" | 1 `location.address`, `location.directions` |
| (04) Pick-up | Opening hours | 1 `company.openingHours` |
| (04) Pick-up | Handover notes 01–03 | Static, by `type` and `fuel` |
| (05) Company | Name, "View company →" | 1 `company.name`, `company.id` (links to the company page) |
| (05) Company | Rating "4.8 ★ 212" | 1 `company.rating`, `company.reviewCount` |
| (05) Company | Rentals "1,240", "1,240 completed rentals" | 1 `company.completedRentals` |
| (05) Company | "Replies in 18 min" | 1 `company.replyTimeMinutes` |
| (05) Company | "On RentXe 5 yrs", "since 2021" | 1 `company.createdAt` |
| (05) Company | "fleet of 16 cars" | 1 `company.fleet` |
| (05) Company | "approves or declines most requests within a day" | Static |
| (06) Reviews | "4.7", stars, "50 reviews of this car" | 1 `reviewSummary` |
| (06) Reviews | Bars for 5 to 1 stars | 1 `reviewSummary.byStars` |
| (06) Reviews | Review cards: stars, quote, "Sarah L.", "28 Oct 2026", "Rented 3 days" | 5 `rating`, `comment`, `authorName`, `createdAt`, `rentalDays` |
| (06) Reviews | "Rated by verified renters only" | Static. True by rule VEH-27. |
| (06) Reviews | "Show all 50 reviews →" | 1 `reviewSummary.count`; links to an all-reviews page (no mockup) |
| Panel | "A$68 / day" | 1 `pricePerDay` |
| Panel | "Free for your dates" / "Booked 11–12 Dec" / "Booked for your dates" | 3 `available`, `bookedDates` |
| Panel | "Free · only 2 left" | Dropped: one listing is one vehicle (question 12). Mockup to-do: show "Free for your dates" |
| Panel | Pick-up "Fri 11 Dec from 10:00", Return "Mon 14 Dec by 10:00 · 3 days" | URL dates; 1 `pickUpTime`, `returnTime`; 3 `days` |
| Panel | Basic cover "Included, Excess A$3,000"; Premium cover "+A$14 / day, Excess A$500" | 1 `insuranceOptions` |
| Panel | "A$68 × 3 days A$204", cover line, "Total A$204" | 3 `pricePerDay`, `rentalAmount`, `insurancePerDay`, `insuranceAmount`, `totalPrice` |
| Panel | "Refundable deposit A$300 · Held at pick-up · not part of the total" | 1 `deposit` |
| Panel | "Next free 3 days · Sun 13 Dec → Wed 16 Dec · A$387 total with basic cover" | 3 `nextAvailable` |
| Panel | **Request to book** | 4 |
| Panel | **Switch to 13–16 Dec** | Static: sets the dates from `nextAvailable`, then calls 3 again |
| Panel | "You won't be charged until the company approves." | Static |
| Panel | Rules: cancellation and fee text, "Draft · SRS §2.8" tag | Static. Must match SRS §2.8. |
| Panel | "Here: free until Thu 10 Dec, 10:00, then A$102" | 3 `cancellation.freeUntil`, `cancellation.feeAfter` |
| Panel | "Here: A$11.33 an hour, at most A$68" | 1 `lateReturnFee.perStartedHour`, `lateReturnFee.max` |
| Phone bar | "A$204 total · 11–14 Dec · 3 days" or "Not free · next free 13–16 Dec" | 3 |
| (07) Similar | "Similar near Melbourne CBD." | Searched place name from the link (static) |
| (07) Similar | Cards: type, kind, name, specs, company and rating, area and km, price, "A$147 est. for 3 days", availability | 6 |
| (07) Similar | "Add to compare" | Compare (search.md) |
| (07) Similar | "View", "All results →" | Static links with the current dates |

## Endpoints

### 1. Vehicle detail

`GET /api/v1/vehicles/{id}`

| | |
|---|---|
| SRS | 2.2 Vehicle management (the listing as customers see it) |
| Access | Public |

Query parameters:

| Name | Type | Required | Rules |
|---|---|---|---|
| `placeId` | long | no | The searched place, an `id` from `GET /api/v1/places` (search.md) |

Response `200`: a **Vehicle** (the README model, including the fields listed under [Changes to shared models](#changes-to-shared-models)), plus these page fields:

| Field | Type | Notes |
|---|---|---|
| `pickUpTime`, `returnTime` | string | Local time at the pick-up place, `"10:00"` (VEH-4) |
| `lateReturnFee` | object | `perStartedHour`, `max`: decimals for this vehicle (VEH-24, VEH-25) |
| `distanceKm` | decimal \| null | _derived_: from the place to the pick-up point, worked out as search.md SR-3. `null` without `placeId`. |
| `reviewSummary` | object | _derived_: reviews of this vehicle only. See below. |
| `company` | object | Company summary. See below. |
| `currency` | string | `"AUD"` |

`reviewSummary`:

| Field | Type | Notes |
|---|---|---|
| `average` | decimal \| null | 1 decimal place. `null` with no reviews. (VEH-28) |
| `count` | int | |
| `byStars` | object | Review count per rating. Keys `"5"` to `"1"`, always all five. |

`company`: the **Company** model (with the proposed `createdAt` and `openingHours`), plus:

| Field | Type | Notes |
|---|---|---|
| `completedRentals` | int | _derived_ (VEH-34) |
| `replyTimeMinutes` | int \| null | _derived_ (VEH-34) |
| `fleet` | object | _derived_: `cars`, `motorbikes`. Listed vehicles by type. |

The company summary is **embedded** rather than a separate call. The page always needs it, one call fills sections (01) to (05), and it leaves `GET /api/v1/companies/{id}` free for the company page to design. The review summary is embedded for the same reason: the title and (06) both need it, and the reviews list stays a plain page.

Example: `GET /api/v1/vehicles/1?placeId=2`

```json
{
  "id": 1,
  "companyId": 1,
  "type": "CAR",
  "brand": "Toyota",
  "model": "Corolla Hybrid",
  "year": 2023,
  "bodyStyle": "SEDAN",
  "transmission": "AUTOMATIC",
  "seats": 5,
  "engineCc": null,
  "fuel": "HYBRID",
  "features": [],
  "pricePerDay": 68.00,
  "location": {
    "area": "Melbourne CBD",
    "city": "Melbourne",
    "address": "212 Flinders Lane, Melbourne VIC 3000",
    "directions": "Front desk, ground floor",
    "lat": -37.8163,
    "lng": 144.9662,
    "timeZone": "Australia/Melbourne"
  },
  "imageUrls": [],
  "listed": true,
  "plateNumber": "1XR·4KD",
  "plateRegion": "VIC",
  "odometerKm": 18420,
  "fuelDetail": "4.4 L / 100 km",
  "bags": 2,
  "helmets": null,
  "minimumAge": 21,
  "deposit": 300.00,
  "insuranceOptions": [
    { "cover": "BASIC", "pricePerDay": 0.00, "excess": 3000.00 },
    { "cover": "PREMIUM", "pricePerDay": 14.00, "excess": 500.00 }
  ],
  "pickUpTime": "10:00",
  "returnTime": "10:00",
  "lateReturnFee": { "perStartedHour": 11.33, "max": 68.00 },
  "distanceKm": 0.8,
  "reviewSummary": {
    "average": 4.7,
    "count": 50,
    "byStars": { "5": 38, "4": 9, "3": 2, "2": 1, "1": 0 }
  },
  "company": {
    "id": 1,
    "name": "Yarra Car Co.",
    "verified": true,
    "rating": 4.8,
    "reviewCount": 212,
    "createdAt": "2021-03-15T00:00:00Z",
    "openingHours": [
      { "days": "Mon – Fri", "hours": "7:00 – 19:00" },
      { "days": "Sat – Sun", "hours": "8:00 – 17:00" }
    ],
    "completedRentals": 1240,
    "replyTimeMinutes": 18,
    "fleet": { "cars": 16, "motorbikes": 0 }
  },
  "currency": "AUD"
}
```

Errors:

| Status | When |
|---|---|
| `400` | Unknown `placeId` |
| `404` | No vehicle with this id, `listed` is `false`, or its company is not live (VEH-35) |

Notes:
- An empty `imageUrls` is normal. The page shows the drawing until the company uploads photos.

### 2. Vehicle availability

`GET /api/v1/vehicles/{id}/availability`

| | |
|---|---|
| SRS | 2.2 Vehicle management (availability), used by 2.4 to pick dates |
| Access | Public |

Query parameters. `from` and `to` here are the calendar window, not rental dates.

| Name | Type | Required | Rules |
|---|---|---|---|
| `from` | date | yes | First day of the window |
| `to` | date | yes | Last day, included. On or after `from`. At most 366 days after `from` (assumption). |

Response `200`:

| Field | Type | Notes |
|---|---|---|
| `vehicleId` | long | |
| `from`, `to` | date | As sent |
| `today` | date | Today at the pick-up place (`location.timeZone`). The page uses it for the today marker and to grey past days. |
| `bookedDates` | date[] | Blocked days in the window, sorted (VEH-6). Days before `today` are left out (VEH-8). |

Example, the Tesla Model 3 (booked 26–29 Nov, 11–12 Dec and 24–31 Dec): `GET /api/v1/vehicles/4/availability?from=2026-11-01&to=2026-12-31`

```json
{
  "vehicleId": 4,
  "from": "2026-11-01",
  "to": "2026-12-31",
  "today": "2026-11-06",
  "bookedDates": [
    "2026-11-26", "2026-11-27", "2026-11-28", "2026-11-29",
    "2026-12-11", "2026-12-12",
    "2026-12-24", "2026-12-25", "2026-12-26", "2026-12-27",
    "2026-12-28", "2026-12-29", "2026-12-30", "2026-12-31"
  ]
}
```

Errors:

| Status | When |
|---|---|
| `400` | Missing or badly formed date, `to` before `from`, or a window over 366 days |
| `404` | No vehicle with this id, or not listed |

### 3. Price quote

`GET /api/v1/vehicles/{id}/quote`

| | |
|---|---|
| SRS | 2.4 Rental booking (the fee rule is §2.8) |
| Access | Public |

Query parameters:

| Name | Type | Required | Rules |
|---|---|---|---|
| `startDate` | date | yes | Pick-up date. After today at the pick-up place (VEH-3). |
| `endDate` | date | yes | Return date. After `startDate` (VEH-2). |
| `insurance` | enum | no | `BASIC` (default) or `PREMIUM` |

Response `200`:

| Field | Type | Notes |
|---|---|---|
| `vehicleId` | long | |
| `startDate`, `endDate` | date | As sent |
| `days` | int | VEH-1 |
| `available` | boolean | `true` when no day in the range is blocked (VEH-7) |
| `bookedDates` | date[] | Blocked days inside the range. Empty when `available` is `true`. |
| `nextAvailable` | object \| null | Only when `available` is `false`: `startDate`, `endDate`, `totalPrice` (with basic cover). `null` if none is found (VEH-9). |
| `insurance` | enum | As sent, or `BASIC` |
| `pricePerDay` | decimal | The vehicle's daily rate |
| `rentalAmount` | decimal | VEH-10 |
| `insurancePerDay` | decimal | `0.00` for `BASIC` |
| `insuranceAmount` | decimal | VEH-11 |
| `totalPrice` | decimal | VEH-12. Worked out even when `available` is `false`. |
| `cancellation` | object | `freeUntil` (timestamp, VEH-22) and `feeAfter` (decimal, VEH-23) |
| `currency` | string | `"AUD"` |

Example, free, with premium cover: `GET /api/v1/vehicles/1/quote?startDate=2026-12-11&endDate=2026-12-14&insurance=PREMIUM`

```json
{
  "vehicleId": 1,
  "startDate": "2026-12-11",
  "endDate": "2026-12-14",
  "days": 3,
  "available": true,
  "bookedDates": [],
  "nextAvailable": null,
  "insurance": "PREMIUM",
  "pricePerDay": 68.00,
  "rentalAmount": 204.00,
  "insurancePerDay": 14.00,
  "insuranceAmount": 42.00,
  "totalPrice": 246.00,
  "cancellation": { "freeUntil": "2026-12-09T23:00:00Z", "feeAfter": 123.00 },
  "currency": "AUD"
}
```

Example, clash (the Tesla is booked 11–12 Dec): `GET /api/v1/vehicles/4/quote?startDate=2026-12-11&endDate=2026-12-14`

```json
{
  "vehicleId": 4,
  "startDate": "2026-12-11",
  "endDate": "2026-12-14",
  "days": 3,
  "available": false,
  "bookedDates": ["2026-12-11", "2026-12-12"],
  "nextAvailable": { "startDate": "2026-12-13", "endDate": "2026-12-16", "totalPrice": 387.00 },
  "insurance": "BASIC",
  "pricePerDay": 129.00,
  "rentalAmount": 387.00,
  "insurancePerDay": 0.00,
  "insuranceAmount": 0.00,
  "totalPrice": 387.00,
  "cancellation": { "freeUntil": "2026-12-09T23:00:00Z", "feeAfter": 193.50 },
  "currency": "AUD"
}
```

Errors:

| Status | When |
|---|---|
| `400` | Missing or badly formed date, `startDate` not after today, `endDate` not after `startDate`, a rental over 30 days or `startDate` more than 365 days after today (VEH-37), unknown `insurance` |
| `404` | No vehicle with this id, or not listed |

Notes:
- Booked dates never give an error here. The quote returns `200` with `available: false`, so the page can show the clash state. Only endpoint 4 returns `409`.
- A quote is not a hold. Someone else can take the dates before the customer sends the request (VEH-19).

### 4. Send a booking request

`POST /api/v1/bookings`

| | |
|---|---|
| SRS | 2.4 Rental booking |
| Access | `CUSTOMER` |

Request body:

| Name | Type | Required | Rules |
|---|---|---|---|
| `vehicleId` | long | yes | A listed vehicle (VEH-17) |
| `startDate` | date | yes | After today at the pick-up place (VEH-3) |
| `endDate` | date | yes | After `startDate` (VEH-2) |
| `insurance` | enum | no | `BASIC` (default) or `PREMIUM` |

Any other field, such as `totalPrice`, is ignored (VEH-15).

Example request:

```json
{
  "vehicleId": 1,
  "startDate": "2026-12-11",
  "endDate": "2026-12-14",
  "insurance": "BASIC"
}
```

Response `201`, with `Location: /api/v1/bookings/1207`. The body is a **Booking** (with the proposed fields) plus `currency`:

```json
{
  "id": 1207,
  "vehicleId": 1,
  "customerId": 42,
  "companyId": 1,
  "startDate": "2026-12-11",
  "endDate": "2026-12-14",
  "status": "REQUESTED",
  "insurance": "BASIC",
  "pricePerDay": 68.00,
  "insurancePerDay": 0.00,
  "excess": 3000.00,
  "deposit": 300.00,
  "totalPrice": 204.00,
  "respondedAt": null,
  "expiresAt": "2026-11-07T08:30:00Z",
  "createdAt": "2026-11-06T08:30:00Z",
  "currency": "AUD"
}
```

Errors:

| Status | When |
|---|---|
| `400` | Missing field, badly formed date, `startDate` not after today, `endDate` not after `startDate`, a rental over 30 days or `startDate` more than 365 days after today (VEH-37), unknown `insurance` |
| `401` | Not logged in. The page sends the customer to log in with `next` set to this URL, so they come back to the same vehicle and dates (login.md LOGIN-29). |
| `403` | Role is not `CUSTOMER`, the account is `SUSPENDED`, or the CSRF header is missing or wrong (login.md LOGIN-36) |
| `404` | No vehicle with `vehicleId`, or not listed |
| `409` | Some of the dates are blocked when the booking is saved (VEH-19, VEH-20). Adds `bookedDates`. |

`409` example. Another customer's request for 10–15 Dec was saved first:

```json
{
  "type": "about:blank",
  "title": "Conflict",
  "status": 409,
  "detail": "These dates are no longer free",
  "instance": "/api/v1/bookings",
  "bookedDates": ["2026-12-11", "2026-12-12", "2026-12-13", "2026-12-14"]
}
```

`400` example:

```json
{
  "type": "about:blank",
  "title": "Bad Request",
  "status": 400,
  "detail": "Validation failed",
  "instance": "/api/v1/bookings",
  "errors": [{ "field": "endDate", "message": "must be after startDate" }]
}
```

Notes:
- When the clash is checked: the quote only reports it. The real check runs in the same transaction that saves the booking, after locking the vehicle row (JPA `@Lock(PESSIMISTIC_WRITE)` on the vehicle, then the overlap query, then the insert). This works on H2 and MySQL.
- Overlap query: a booking for the same vehicle that is `APPROVED` or `PICKED_UP`, or `REQUESTED` with `expiresAt > now` (VEH-36), with `startDate <= :endDate` and `endDate >= :startDate`.
- On `409` the page reloads availability and the quote, then shows the unavailable state with the next free dates.
- On `201` the page opens the new booking (assumption: on the My bookings page, not designed yet).
- The button is disabled while the request is in flight. A repeat of the same request gets `409`, because the customer's own `REQUESTED` booking blocks the dates.
- Insurance does change the Booking model. See [Changes to shared models](#changes-to-shared-models).

### 5. Reviews of the vehicle

`GET /api/v1/vehicles/{id}/reviews`

| | |
|---|---|
| SRS | 2.6 Reviews and ratings |
| Access | Public |

Query parameters:

| Name | Type | Required | Rules |
|---|---|---|---|
| `page` | int | no | Default `0` |
| `size` | int | no | Default `20`, 1 to 50 (assumption). The page asks for `6`. |
| `sort` | string | no | `createdAt` or `rating`, with `asc` or `desc`. Default `createdAt,desc` (VEH-30). |

Response `200`: a page. Each item has the **Review** fields `id`, `rating`, `comment`, `createdAt`, plus:

| Field | Type | Notes |
|---|---|---|
| `authorName` | string | _derived_ (VEH-29) |
| `rentalDays` | int | _derived_: `endDate − startDate` of the review's booking |

`authorId`, `bookingId`, `vehicleId` and `companyId` are left out, because the endpoint is public.

Example: `GET /api/v1/vehicles/1/reviews?page=0&size=6&sort=createdAt,desc` (2 of 6 items shown)

```json
{
  "content": [
    {
      "id": 318,
      "rating": 5,
      "comment": "Exactly as listed, down to the odometer. The walk-around photos made the return take two minutes.",
      "authorName": "Sarah L.",
      "rentalDays": 3,
      "createdAt": "2026-10-28T03:12:00Z"
    },
    {
      "id": 301,
      "rating": 5,
      "comment": "Comfortable for four adults and our bags. The request was approved in under an hour.",
      "authorName": "Tom W.",
      "rentalDays": 7,
      "createdAt": "2026-10-17T09:40:00Z"
    }
  ],
  "page": { "size": 6, "number": 0, "totalElements": 50, "totalPages": 9 }
}
```

Errors:

| Status | When |
|---|---|
| `400` | `size` out of range, or an unknown `sort` field |
| `404` | No vehicle with this id, or not listed |

Notes:
- The average, count and star bars come from `reviewSummary` in endpoint 1.
- Writing a review is not on this page (My reviews, not designed yet). Rule VEH-27 applies there.
- "Show all 50 reviews →" opens an all-reviews page (no mockup) that pages through this endpoint.

### 6. Similar vehicles

`GET /api/v1/vehicles/{id}/similar`

| | |
|---|---|
| SRS | 2.3 Vehicle search and comparison |
| Access | Public |

Query parameters:

| Name | Type | Required | Rules |
|---|---|---|---|
| `startDate`, `endDate` | date | yes | Same rules as the quote (VEH-2, VEH-3) |
| `placeId` | long | no | Searched place, as in endpoint 1. Adds `distanceKm`. |
| `size` | int | no | Default `3`, 1 to 6 (assumption) |

The order is fixed (VEH-31), so there is no `sort`.

Response `200`: a page, plus `currency`. Each item is a **SearchResult**, the search page's row shape (search.md), so the card and "Add to compare" work the same in both places. `totalPrice` is the basic-cover total (VEH-33). `availability` follows VEH-6 and VEH-7; the card shows "Booked 11–12 Dec" from `bookedRanges`.

Example: `GET /api/v1/vehicles/1/similar?startDate=2026-12-11&endDate=2026-12-14&placeId=2` (third of 3 items shown; the Suzuki Swift and Mazda CX-5 come first, both free)

```json
{
  "content": [
    {
      "id": 4,
      "type": "CAR",
      "brand": "Tesla",
      "model": "Model 3",
      "year": 2024,
      "bodyStyle": "SEDAN",
      "transmission": "AUTOMATIC",
      "seats": 5,
      "engineCc": null,
      "fuel": "ELECTRIC",
      "fuelDetail": "510 km range",
      "bags": null,
      "helmets": null,
      "features": [],
      "pricePerDay": 129.00,
      "imageUrl": null,
      "location": { "area": "Richmond", "lat": -37.8230, "lng": 145.0000 },
      "company": { "id": 3, "name": "Laneway Motors", "rating": 4.4, "reviewCount": 96 },
      "distanceKm": 3.4,
      "rentalDays": 3,
      "totalPrice": 387.00,
      "availability": {
        "status": "BOOKED",
        "bookedRanges": [{ "startDate": "2026-12-11", "endDate": "2026-12-12" }]
      }
    }
  ],
  "page": { "size": 3, "number": 0, "totalElements": 3, "totalPages": 1 },
  "currency": "AUD"
}
```

Errors:

| Status | When |
|---|---|
| `400` | Bad dates (as in the quote), unknown `placeId`, or `size` out of range |
| `404` | No vehicle with this id, or not listed |

Notes:
- The card uses the search page's card design, so the endpoint returns the same SearchResult shape as search.

## Endpoints used from other pages

| Page part | Endpoint | Defined in |
|---|---|---|
| Nav: first name, initials, full name, email | `GET /api/v1/auth/me` | login.md |
| Nav: Log out | The log-out endpoint under `/api/v1/auth/*` | login.md |
| Nav: "My bookings 02" | Active-booking count | search.md |
| Similar cards: "Add to compare" (up to 3) | Compare | search.md |
| "Back to results", "All results →" | Vehicle search. This page only builds the link. | search.md |
| "View company →" | The company page, by `company.id`. No mockup yet; its API is not designed here. | — |
| After a request: the booking | `GET /api/v1/bookings/{id}` (the `Location` header) | My bookings page, not designed yet |

## Validation and business rules

Numbered so the SRS can use them. Rules marked §2.8 go into SRS §2.8. The examples are test cases.

### Dates

| # | Rule |
|---|---|
| VEH-1 | `days` = `endDate − startDate` in calendar days. 11 Dec → 14 Dec is 3 days. |
| VEH-2 | `endDate` must be after `startDate`. A request with the same date for both gets `400`. |
| VEH-3 | `startDate` must be after today, where today is the date at the pick-up place (`location.timeZone`). On 6 Nov 2026 in Melbourne, 6 Nov gets `400` and 7 Nov is accepted. |
| VEH-37 | A booking is 1 to 30 days long (VEH-1), and `startDate` is at most 365 days after today (VEH-3's today). Otherwise `400`: "A rental can be at most 30 days" on `endDate`, or "Pick-up can be at most 12 months ahead" on `startDate`. The same for every company. Longer rentals use extensions (VEH-38). Page: the date pickers stop at these limits. |
| VEH-4 | Pick-up is from 10:00 on `startDate`. Return is by 10:00 on `endDate`. Local time at the pick-up place. Assumption: the same for every vehicle. |
| VEH-5 | Pick-up and return are at the same place: the vehicle's `location`. |

### Availability

| # | Rule |
|---|---|
| VEH-6 | A booking with status `REQUESTED` (until its `expiresAt`, VEH-36), `APPROVED` or `PICKED_UP` blocks every day from its `startDate` to its `endDate`, both included. `REJECTED`, `CANCELLED`, `EXPIRED` and `RETURNED` bookings block nothing. A waiting extension also blocks its extra days (VEH-38). |
| VEH-7 | A date range is free when none of its days, both ends included, is blocked. With a booking for 11–12 Dec: 10–11 Dec clashes, 12–15 Dec clashes, 13–16 Dec is free. |
| VEH-8 | The calendar shows blocked days only as "Booked". It never shows who booked or the booking status. Days before today are not returned. |
| VEH-9 | Next free dates: try each start date after the chosen `startDate` (and after today), up to 240 days ahead. The first one whose range of the same length is free wins. If none is free, there is no suggestion. Tesla booked 11–12 Dec, chosen 11–14 Dec: next free is 13–16 Dec. |

### Price (§2.8 fee rule)

| # | Rule |
|---|---|
| VEH-10 | `rentalAmount` = `pricePerDay × days`. |
| VEH-11 | Basic cover is included: `insuranceAmount` is `0.00`. Premium cover: `insuranceAmount` = the premium `pricePerDay × days`. |
| VEH-12 | `totalPrice` = `rentalAmount + insuranceAmount`. Nothing else is added: no service fee, no young-driver fee. Corolla Hybrid, 3 days: `204.00` with basic cover, `246.00` with premium. |
| VEH-13 | The deposit is not part of `totalPrice`. It is held at pick-up and refunded at return (§2.5). |
| VEH-14 | Amounts are rounded to 2 decimal places, half up. Assumption. |
| VEH-15 | The server works out the price when it saves the booking, from the vehicle's prices at that moment. It ignores any price or total in the request body. It stores the rates and `totalPrice` on the booking, so a later price change does not change the booking. |

### Booking request

| # | Rule |
|---|---|
| VEH-16 | Only a logged-in `CUSTOMER` with status `ACTIVE` can send a request. Not logged in: `401`. Other role or suspended: `403`. |
| VEH-17 | The vehicle must exist, be listed and belong to a live company (VEH-35). Otherwise `404`. |
| VEH-18 | The dates must pass VEH-2, VEH-3 and VEH-37. Otherwise `400`. |
| VEH-19 | The dates must be free (VEH-7) when the booking is saved. Otherwise `409` with the blocked days. A quote does not hold the dates. |
| VEH-20 | If two requests for overlapping dates on one vehicle arrive together, the first to be saved gets `201` and the other gets `409`. This also applies when the same customer sends the same request twice. |
| VEH-21 | A new booking starts as `REQUESTED`, with `expiresAt` set by VEH-36. The customer is not charged until the company approves (page text). |
| VEH-36 | A `REQUESTED` booking expires if the company has not approved or rejected it by its `expiresAt`: 24 hours after `createdAt`, or the start of the pick-up day (00:00 in `location.timeZone`) if that is sooner. It becomes `EXPIRED`, frees its dates, and no longer counts as active. A scheduled job marks expired requests every 15 minutes. Until it runs, the clash check (VEH-19), the calendar, search and `GET /bookings/summary` already treat a `REQUESTED` booking past its `expiresAt` as expired. The company cannot approve it after `expiresAt` (`409`). The customer sees "The company didn't answer in time". Example: sent Tue 18:00 for Thu to Sun, it expires Wed 18:00; sent Tue 18:00 for Wed, it expires Wed 00:00. |

### Cancellation (§2.8). Enforced on My bookings, shown here.

| # | Rule |
|---|---|
| VEH-22 | Cancelling is free until 24 hours before pick-up (VEH-4). Pick-up Fri 11 Dec 10:00 in Melbourne: free until Thu 10 Dec 10:00 (`2026-12-09T23:00:00Z`). |
| VEH-23 | After that, the fee is 50% of `totalPrice`. `204.00` → `102.00`. `387.00` → `193.50`. |

### Extending a rental (§2.4, §2.8). Enforced on My bookings (no mockup yet), described here.

| # | Rule |
|---|---|
| VEH-38 | The customer can ask to extend a `PICKED_UP` booking, from 7 days before its `endDate` until the day before it (dates at the pick-up place). The new return date is 1 to 30 days after the current `endDate`, so each extension adds at most 30 days, with no limit on how many. Only one extension can wait at a time. The extra days (the day after `endDate` to the new return date) must be free (VEH-6, VEH-7), otherwise `409`. A waiting extension holds those days and expires like a request (VEH-36): 24 hours after it is sent, or at 00:00 on the current `endDate` if sooner. The company approves or rejects it; the customer can withdraw it while it waits. On approval, the booking's `endDate` becomes the new date and its `totalPrice` grows by extra days × (`pricePerDay` + `insurancePerDay`), the booking's own rates. The deposit doesn't change, and the late fee (VEH-24) counts from the new return date. It stays one booking, with one pick-up, one return and one review. Example: 1 to 31 Dec at `68.00`, basic cover. Between 24 and 30 Dec Minh asks for 30 Jan; on approval the total grows by 30 × `68.00` = `2,040.00`. From 23 Jan he can ask again. |

### Late return (§2.8). Enforced at return (§2.5), shown here.

| # | Rule |
|---|---|
| VEH-24 | Each started hour after the return time costs `pricePerDay ÷ 6`, rounded to cents first. At `68.00` a day that is `11.33` an hour. 2 h 10 min late = 3 started hours = `33.99`. |
| VEH-25 | The late fee is capped at one `pricePerDay`. At `68.00` a day, 7 hours late costs `68.00`, not `79.31`. |

### Reviews

| # | Rule |
|---|---|
| VEH-26 | Section (06) lists only reviews of this vehicle. The company rating in (05) averages the reviews of all the company's vehicles. |
| VEH-27 | Only the customer of a `RETURNED` booking can review it, once per booking. So every review shown comes from a verified renter. |
| VEH-28 | `average` is the mean rating, 1 decimal place, `null` with no reviews. 38 × 5, 9 × 4, 2 × 3 and 1 × 2 over 50 reviews = 4.68 → `4.7`. |
| VEH-29 | The author is shown as first name plus last-name initial: "Sarah Lee" → "Sarah L.". A one-word name is shown as is. Full name, email and user id are never returned. |
| VEH-30 | Reviews are listed newest first unless `sort` says otherwise. |

### Similar vehicles

| # | Rule |
|---|---|
| VEH-31 | Up to 3 listed vehicles in the same `location.city`, not this one. Same `type` first, then the smallest difference in `pricePerDay`, then the lowest `id` (assumption). Corolla Hybrid (`68.00`): Suzuki Swift (`49.00`), Mazda CX-5 (`94.00`), Tesla Model 3 (`129.00`). |
| VEH-32 | Vehicles booked on the chosen dates still appear, with their booked days. |
| VEH-33 | A similar card's `totalPrice` = `pricePerDay × days`, with basic cover. |

### Company stats and visibility

| # | Rule |
|---|---|
| VEH-34 | `completedRentals` = the company's `RETURNED` bookings. `fleet` = its listed vehicles by type. `replyTimeMinutes` = the median minutes from `createdAt` to `respondedAt` over the company's bookings answered in the last 90 days, `null` if none (assumption). |
| VEH-35 | A vehicle with `listed: false`, or whose company is not live (not `verified`, or its account is `SUSPENDED`; login.md LOGIN-26, LOGIN-27), returns `404` from every endpoint in this file and cannot be requested. Its own company and admins can still read it. |

## Changes to shared models

Merged into the README on 2026-11-06. Kept here as the reason for each field.

### Vehicle: add

| Field | Type | Notes |
|---|---|---|
| `plateNumber` | string | As on the plate, for example `1XR·4KD`, `59-X1 234.56` |
| `plateRegion` | string | State or country that issued the plate, for example `VIC`, `VN` |
| `odometerKm` | int | Reading at the last return. Updated by the return flow (§2.5). |
| `fuelDetail` | string \| null | Consumption, tank size or electric range, for example `4.4 L / 100 km`, `510 km range` |
| `bags` | int \| null | Cars: large bags that fit. Replaces `"2 bags"` in `features`. |
| `helmets` | int \| null | Motorbikes: helmets supplied. Replaces `"2 helmets"` in `features` (the README's example). |
| `minimumAge` | int | Youngest allowed driver or rider, for example `21` |
| `deposit` | decimal | Refundable, held at pick-up, not part of `totalPrice` |
| `insuranceOptions` | InsuranceOption[] | Exactly one `BASIC` and one `PREMIUM` |

InsuranceOption:

| Field | Type | Notes |
|---|---|---|
| `cover` | enum | `BASIC`, `PREMIUM` |
| `pricePerDay` | decimal | Always `0.00` for `BASIC` |
| `excess` | decimal | Most the customer pays towards damage, for example `3000.00` basic, `500.00` premium |

### Location: add

| Field | Type | Notes |
|---|---|---|
| `directions` | string \| null | How to find the desk, for example `Front desk, ground floor` |
| `timeZone` | string | IANA zone, for example `Australia/Melbourne`, `Asia/Ho_Chi_Minh`. Sets "today" (VEH-3) and the 10:00 times (VEH-4, VEH-22). |

### Company: add

| Field | Type | Notes |
|---|---|---|
| `createdAt` | timestamp | "On RentXe since 2021" |
| `openingHours` | object[] | Display text: `{ "days": "Mon – Fri", "hours": "7:00 – 19:00" }`. See open question 6. |

### Booking: add

| Field | Type | Notes |
|---|---|---|
| `insurance` | enum | `BASIC` (default), `PREMIUM` |
| `pricePerDay` | decimal | The vehicle's daily rate when the request was saved |
| `insurancePerDay` | decimal | The cover's daily price then. `0.00` for `BASIC`. |
| `excess` | decimal | The chosen cover's excess then |
| `deposit` | decimal | The vehicle's deposit then |
| `respondedAt` | timestamp \| null | When the company approved or rejected. Used for `replyTimeMinutes`. |
| `expiresAt` | timestamp | _derived_ once when the request is saved (VEH-36), then stored |

### Booking: change

| Field | Change |
|---|---|
| `totalPrice` | Still _derived_, but worked out once when the request is saved (VEH-12, VEH-15) and stored. Never recomputed from the vehicle's current price. |
| `status` | Add `EXPIRED`: a request the company did not answer by `expiresAt` (VEH-36) |
| `endDate` | Moves later when an extension is approved (VEH-38). A new table, BookingExtension, keeps each extension request (README). |

Review needs no change. `authorName` and `rentalDays` are derived in endpoint 5.

## Open questions

1. **Do pending requests hold dates?** Resolved 2026-11-06 ([decision](../decisions/requests-hold-dates-and-expire.md)): yes. `REQUESTED` blocks its days (VEH-6), so the first request wins and an approval never clashes. README decision 1.
2. **Unanswered requests.** Resolved 2026-11-06 ([decision](../decisions/requests-hold-dates-and-expire.md)): a request expires 24 hours after it is sent, or at the start of the pick-up day if sooner, and becomes `EXPIRED` (VEH-36).
3. **Same-day turnaround.** Resolved 2026-11-06 ([decision](../decisions/return-day-stays-blocked.md)): no. The return day stays blocked (VEH-7), so the next pick-up is the day after at the earliest. README decision 3.
4. **Pick-up today.** The date fields and the URL check make tomorrow the earliest pick-up (VEH-3), but the calendar lets you click today. Which is right? The mockup should match. README decision 2.
5. **Limits.** Resolved 2026-11-06 ([decision](../decisions/rental-length-and-horizon.md)): a booking is at most 30 days and starts at most 12 months ahead (VEH-37). Longer rentals are extended 30 days at a time from the last week of the rental, with the company's approval ([decision](../decisions/extend-rental-by-30-days.md), VEH-38).
6. **Pick-up time and opening hours.** Is 10:00 fixed for every vehicle, or set by the company? Southbank Rentals is closed on Sundays, yet a Sunday 10:00 pick-up is allowed. Block closed days? If so, opening hours need real times instead of display text. Also: hours per company (the mockup) or per pick-up place?
7. **Insurance.** Who sets the premium price and the excess amounts: the company for each vehicle (this file) or RentXe for each vehicle class? Who is the insurer?
8. **Payment.** The page says "You won't be charged until the company approves", and the rules charge cancellation and late fees. The brief does not mention payment. Does RentXe only record amounts owed, or take payment?
9. **Late return over 24 hours.** The fee is capped at one daily rate (VEH-25). Does the cap hold however late the return is, or does each further day add a daily rate?
10. **Age and licence.** User has no date of birth or licence type, so the server cannot check `minimumAge` or the licence. Check at pick-up only (this file's assumption), or add the fields and check at request time?
11. **Price change between quote and request.** The server charges the current price and ignores the client's total (VEH-15). Should it instead return `409` when the total differs from the one the customer saw?
12. **"Only 2 left".** Resolved 2026-11-06 ([decision](../decisions/one-listing-one-vehicle.md)): each listing is one vehicle with one plate, so there is nothing to count. The badge is dropped here and in search (search.md Q1, SR-8).
13. **Card shape.** Resolved: endpoint 6 returns search.md's SearchResult.
14. **Confirm step.** The button's link (`#booking?id=…&from=…&to=…&cover=…`) suggests a confirm page before the request is sent. Is there one? The API is the same either way.
15. **Searched place.** Resolved: the search page adds `placeId` to the View link, and this page reads the place's name and point from search.md's places endpoint.
16. **Login.** This file makes the read endpoints public so shared links work. Does the page itself require a login, or only the **Request to book** button?
