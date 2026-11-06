# Search (customer)

Customers find a car or motorbike near a place for their dates, narrow the list with filters, and pick up to three to compare.

Mockup: `assets/mockups/search/index.html`. It is the first page a customer sees after logging in. The landing page's search form also opens it.

## States and URL parameters

The mockup uses fake data: 8 listings near Melbourne CBD, 4 near District 1 in Ho Chi Minh City, and fixed dates of 11–14 Dec 2026.

| Parameter | Mockup | Real app |
|---|---|---|
| `?view=list` (default) | Results as rows | Same |
| `?view=map` | Results as price pins on a map, with a short list and a card for the picked pin | Same |
| `?view=empty` | Sets filters that match nothing (Manual, up to A$50 a day, rated 4.5+), so the "Loosen one filter" list shows | Not a mode. The page shows the empty state whenever a search returns 0 results |
| `?city=hcm` | Switches to the Ho Chi Minh City data | Replaced by `placeId` |
| `?filters=open` | Opens the filter sheet on load, on screens 960px wide or less | Same. UI only |
| `?compare=mel-01,mel-03` | Ticks up to 3 listings from the same city | Same, with vehicle IDs: `?compare=1,3` |

Real app (proposal): the page keeps the whole search in its query string, using the API parameter names below (except the dates, which stay `from` and `to` as in the mockup's links), so a search survives a reload and can be shared. Example: `?placeId=2&from=2026-12-11&to=2026-12-14&type=CAR&maxPrice=100&sort=price,asc&view=map&compare=1,3`.

Hand-off from the landing page (landing.md): `?type=MOTORBIKE&location=District%201%2C%20Ho%20Chi%20Minh%20City&from=2026-12-11&to=2026-12-14`. The page reads all four.

| Landing parameter | The search page |
|---|---|
| `location` | Turns the text into a place by SR-1, then shows `placeId` in its URL instead. Missing: uses the default place, Melbourne CBD (assumption) |
| `type` | Uses it as the `type` filter |
| `from`, `to` | Uses them as the dates. Missing: tomorrow and three days after, as landing rule LP-2 |

IDs in the examples: mockup listings `mel-01` to `mel-08` are vehicles 1 to 8, and `hcm-01` to `hcm-04` are 9 to 12. Companies: Yarra Car Co. 1, Southbank Rentals 2, Laneway Motors 3, Tullamarine Drive 4, Two Wheels Melbourne 5, Saigon Wheels Co. 6, Ben Thanh Scooters 7, Tan Son Nhat Auto 8. The coordinates are made up but match the mockup's distances.

## What the page shows

"search" is `GET /api/v1/vehicles/search`. "facets" is `GET /api/v1/vehicles/search/facets`.

| UI element | Endpoint | Field |
|---|---|---|
| Nav: first name "Minh", avatar "MT" | `GET /api/v1/auth/me` (login.md) | `fullName` (SR-23) |
| Account menu: "Minh Tran", email, "Customer account" | `GET /api/v1/auth/me` (login.md) | `fullName`, `email`, `role` |
| Nav and account menu: "My bookings 02" | `GET /api/v1/bookings/summary` | `activeCount` (SR-24) |
| Account menu: Log out | `POST /api/v1/auth/logout` (login.md) | none |
| Account menu: Profile, My reviews, Settings; nav: Help | none | Later pages |
| Where field and its suggestions | `GET /api/v1/places` | `content[].label`. The picked `id` is sent as `placeId` |
| Pick-up and Return dates | none (page state) | Sent as `startDate` and `endDate` |
| Headline "8 vehicles near Melbourne CBD." | search; facets | `page.totalElements`; `place.name` |
| Trip line "Fri 11 Dec → Mon 14 Dec · 3 days · 8 listed in total" | facets | Dates from page state; days per SR-5; `nearbyCount` |
| Filter 01 Type: All, Cars, Motorbikes | search, facets | `type` parameter. No counts |
| Filter 02 Price per day: histogram, two-thumb slider, "A$35 … A$140+" | facets | `price.min`, `price.max`, `price.histogram` |
| Filter 03 Brand: checkboxes with counts | facets | `brands[].value`, `brands[].count` |
| Filter 04 Location: Any, 2 km, 5 km, 10 km | search, facets | `maxDistanceKm` parameter. No counts |
| Filter 04 Location: area checkboxes with counts | facets | `areas[].value`, `areas[].count` |
| Filter 05 Transmission | search, facets | `transmission` parameter. No counts |
| Filter 06 Seats (cars) or Engine size (motorbikes) | search, facets | `minSeats`, or `minEngineCc` and `maxEngineCc`. No counts |
| Filter 07 Company rating: radios with counts | facets | `ratings[].minRating`, `ratings[].count` |
| Active filter tags, Clear all, filter count on the phone "Filters" button | none (page state) | |
| "(03) Results · 08"; phone sheet button "Show 8 vehicles" | search | `page.totalElements` |
| Sort menu | search | `sort` parameter |
| List / Map toggle | none | `view` in the page URL |
| Row: photo tile, "Car" or "Motorbike" | search | `imageUrl`, `type` |
| Row: "Sedan · 2023", "Sedan · Electric · 2024" | search | `bodyStyle`, `fuel` (when `ELECTRIC`), `year` |
| Row: "Toyota Corolla Hybrid" | search | `brand`, `model` |
| Row: specs "Automatic / 5 seats / Hybrid / 2 bags", "157 cc / Automatic / 2 helmets" | search | `transmission`, `seats` (cars), `engineCc` (motorbikes), `fuel`, `fuelDetail`, `bags` (cars), `helmets` (motorbikes), `features` |
| Row: "Yarra Car Co. ★ 4.8 (212)" | search | `company.name`, `company.rating`, `company.reviewCount` |
| Row: "Melbourne CBD · 0.8 km away" | search | `location.area`, `distanceKm` |
| Row: "A$68 / day" | search | `pricePerDay` |
| Row: "A$204 est. for 3 days" | search | `totalPrice`, `rentalDays` |
| Row: "Free for your dates", "Only 2 left", "Booked 11–12 Dec" | search | `availability.status`, `availability.unitsLeft`, `availability.bookedRanges` |
| Row: Compare checkbox | none (page state) | `id` |
| Row: View button | Link to the vehicle page | `../vehicle/index.html?id={id}&from={from}&to={to}&placeId={placeId}`. `placeId` lets the vehicle page show the distance and the "Your search" marker |
| List end: "End of results · 8 of 8 listings near Melbourne CBD", "3 hidden by your filters" | search; facets | `page.totalElements`; `nearbyCount` minus `page.totalElements` |
| Map: price pins, outlined when booked | search with `size=100` | `location.lat`, `location.lng`, `pricePerDay`, `availability.status` |
| Map: "you" dot, 2 / 5 / 10 km rings, "Melbourne CBD · not to scale" | facets | `place.lat`, `place.lng`, `place.name` |
| Map: short list and the picked vehicle's card | search | Same row fields as the list |
| Empty state: "8 vehicles are listed near Melbourne CBD for 11 Dec – 14 Dec, but none of them match…" | facets | `nearbyCount`, `place.name` |
| Empty state: "Remove "Manual" +2 vehicles →" | facets | `relaxations[]` |
| Empty state: "Clear all filters +8 vehicles →" | facets | `nearbyCount` |
| Compare tray slots: "Toyota Corolla Hybrid · Yarra Car Co. · A$68/day" | Rows the page already has; `GET /api/v1/vehicles/compare` after a reload | `brand`, `model`, `company.name`, `pricePerDay` |
| Compare tray: "Compare 2" button | Link to the compare page (no mockup yet) | `ids`, `from`, `to`, `placeId` |

## Endpoints

| Method and path | Purpose | SRS | Access |
|---|---|---|---|
| `GET /api/v1/vehicles/search` | Result rows for a place, dates, filters and sort | 2.3 | Public |
| `GET /api/v1/vehicles/search/facets` | Filter options with counts, price bounds, empty-state suggestions | 2.3 | Public |
| `GET /api/v1/vehicles/compare` | Up to 3 vehicles side by side for the dates | 2.3 | Public |
| `GET /api/v1/places` | Suggestions for the Where field. The landing page uses it too | 2.3 | Public |
| `GET /api/v1/places/{id}` | One place, to refill the Where field from `placeId` after a reload. The vehicle page uses it too | 2.3 | Public |
| `GET /api/v1/bookings/summary` | The current customer's active booking count, for the nav | 2.4 | `CUSTOMER` |

Search works logged out. The search, facets, compare and place endpoints are Public, so the landing page and visitors can search. Booking needs a login (vehicle.md). Whether the search page itself needs a login is open question 6.

Why `/vehicles/search` and not `GET /vehicles?…`: a row is a search-only shape (distance, total and availability for the dates). This leaves `GET /vehicles` free for the listing-management pages and `/vehicles/{id}` for vehicle.md. Spring matches the fixed path `/vehicles/search` before `/vehicles/{id}`.

### Shapes defined on this page

#### SearchResult (one row)

A read-only view of a Vehicle and its Company. It holds only what this page shows, plus fields worked out for the place and dates. Field names and types match the shared models.

| Field | Type | Notes |
|---|---|---|
| `id`, `type`, `brand`, `model`, `year`, `bodyStyle`, `transmission`, `seats`, `engineCc`, `fuel`, `fuelDetail`, `bags`, `helmets`, `features`, `pricePerDay` | | From `Vehicle` |
| `imageUrl` | string \| null | First of `Vehicle.imageUrls`. With `null` the page draws a silhouette for the `type` |
| `location` | object | `area`, `lat`, `lng` from `Vehicle.location` |
| `company` | object | `id`, `name`, `rating`, `reviewCount` from `Company` |
| `distanceKm` | decimal \| null | _derived_: SR-3. `null` only from compare called without `placeId` |
| `rentalDays` | int | _derived_: SR-5 |
| `totalPrice` | decimal | _derived_: SR-5 |
| `availability` | Availability | _derived_ for the dates: SR-6 to SR-8 |

#### Availability

| Field | Type | Notes |
|---|---|---|
| `status` | enum | `AVAILABLE`, `FEW_LEFT`, `BOOKED` |
| `unitsLeft` | int \| null | Set only with `FEW_LEFT`. Needs open question 1, option A |
| `bookedRanges` | `{ startDate, endDate }[]` | Set only with `BOOKED`, otherwise `[]` |

#### Place

A shared model now: see [README.md](README.md#place).

### 1. Search vehicles

`GET /api/v1/vehicles/search` · SRS 2.3 · Public

| Parameter | Type | Required | Allowed values | Default |
|---|---|---|---|---|
| `placeId` | long | yes | An `id` from `GET /api/v1/places` | |
| `startDate` | date | yes | After today (SR-4) | |
| `endDate` | date | yes | After `startDate` | |
| `type` | enum | no | `CAR`, `MOTORBIKE` | Both |
| `minPrice` | decimal | no | 0 or more | No lower bound |
| `maxPrice` | decimal | no | `minPrice` or more | No upper bound |
| `brand` | string, repeatable | no | Brand names from facets: `brand=Honda&brand=Vespa` | Any brand |
| `maxDistanceKm` | decimal | no | More than 0. The page sends 2, 5 or 10 | Any distance |
| `area` | string, repeatable | no | Area names from facets | Any area |
| `transmission` | enum | no | `AUTOMATIC`, `MANUAL` | Both |
| `minSeats` | int | no | 1 to 20. The page sends 4, 5 or 7 | Any |
| `minEngineCc` | int | no | 0 or more. The page sends 126 | No lower bound |
| `maxEngineCc` | int | no | `minEngineCc` or more. The page sends 125 or 160 | No upper bound |
| `minRating` | decimal | no | 1.0 to 5.0. The page sends 4.0, 4.5 or 4.8 | Any |
| `sort` | string | no | `recommended`, `price,asc`, `price,desc`, `rating,desc`, `distance,asc` (SR-18) | `recommended` |
| `page` | int | no | 0 or more | 0 |
| `size` | int | no | 1 to 100 | 20 |

Example: Melbourne CBD, 11–14 Dec, cars only, most expensive first, 3 a page.

`GET /api/v1/vehicles/search?placeId=2&startDate=2026-12-11&endDate=2026-12-14&type=CAR&sort=price,desc&size=3`

```json
{
  "content": [
    {
      "id": 7,
      "type": "CAR",
      "brand": "Kia",
      "model": "Carnival",
      "year": 2023,
      "bodyStyle": "PEOPLE_MOVER",
      "transmission": "AUTOMATIC",
      "seats": 8,
      "engineCc": null,
      "fuel": "DIESEL",
      "fuelDetail": null,
      "bags": 5,
      "helmets": null,
      "features": [],
      "pricePerDay": 139.00,
      "imageUrl": "/media/vehicles/7/1.jpg",
      "location": { "area": "Melbourne Airport", "lat": -37.6678, "lng": 144.8410 },
      "company": { "id": 4, "name": "Tullamarine Drive", "rating": 4.2, "reviewCount": 310 },
      "distanceKm": 19.5,
      "rentalDays": 3,
      "totalPrice": 417.00,
      "availability": { "status": "AVAILABLE", "unitsLeft": null, "bookedRanges": [] }
    },
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
      "imageUrl": "/media/vehicles/4/1.jpg",
      "location": { "area": "Richmond", "lat": -37.8230, "lng": 145.0000 },
      "company": { "id": 3, "name": "Laneway Motors", "rating": 4.4, "reviewCount": 96 },
      "distanceKm": 3.4,
      "rentalDays": 3,
      "totalPrice": 387.00,
      "availability": {
        "status": "BOOKED",
        "unitsLeft": null,
        "bookedRanges": [{ "startDate": "2026-12-11", "endDate": "2026-12-12" }]
      }
    },
    {
      "id": 3,
      "type": "CAR",
      "brand": "Mazda",
      "model": "CX-5",
      "year": 2022,
      "bodyStyle": "SUV",
      "transmission": "AUTOMATIC",
      "seats": 5,
      "engineCc": null,
      "fuel": "PETROL",
      "fuelDetail": null,
      "bags": 4,
      "helmets": null,
      "features": [],
      "pricePerDay": 94.00,
      "imageUrl": "/media/vehicles/3/1.jpg",
      "location": { "area": "Southbank", "lat": -37.8270, "lng": 144.9560 },
      "company": { "id": 2, "name": "Southbank Rentals", "rating": 4.6, "reviewCount": 148 },
      "distanceKm": 1.6,
      "rentalDays": 3,
      "totalPrice": 282.00,
      "availability": { "status": "FEW_LEFT", "unitsLeft": 2, "bookedRanges": [] }
    }
  ],
  "page": { "size": 3, "number": 0, "totalElements": 5, "totalPages": 2 },
  "currency": "AUD"
}
```

Errors:

| Status | When |
|---|---|
| `400` | `placeId`, `startDate` or `endDate` missing; unknown `placeId`; a date not in ISO form; `endDate` not after `startDate`; `startDate` not after today; an unknown enum value; `minPrice` above `maxPrice`; `minEngineCc` above `maxEngineCc`; `sort` not in the list; `size` above 100 |

```json
{
  "type": "about:blank",
  "title": "Bad Request",
  "status": 400,
  "detail": "Validation failed",
  "instance": "/api/v1/vehicles/search",
  "errors": [{ "field": "to", "message": "must be after from" }]
}
```

Notes:

- The list view asks for `size=20` and adds the next page with a "Show more" button (assumption: the mockup has 8 rows and no paging control). The map view asks once with `size=100` so every result gets a pin.
- The `sort` keys are worked out, not entity fields: the rating comes from the company and the distance from the place. Bind `sort` as a plain string, not through Spring's `Pageable` sort.
- Dates change totals and availability only, never which vehicles match. So a date change reloads search but not facets.

### 2. Filter options and counts (facets)

`GET /api/v1/vehicles/search/facets` · SRS 2.3 · Public

Facets come from their own endpoint, not inside the search response, because:

- the search response keeps the README's standard paged shape;
- facets do not depend on the dates, the sort or the page, so changing those reloads search only;
- the counts need one count per filter group (and per active filter for the empty state), which the result rows do not.

When a filter changes, the page calls search and facets at the same time. Both take the same filter parameters, so one Java `SearchFilter` object can back both. The scope is one city, typically tens to a few hundred vehicles, so the service can load it once and filter, count and sort in memory.

Parameters: the filter parameters of search: `placeId` (required), `type`, `minPrice`, `maxPrice`, `brand`, `maxDistanceKm`, `area`, `transmission`, `minSeats`, `minEngineCc`, `maxEngineCc`, `minRating`. Same rules. No `from`, `to`, `sort`, `page` or `size`.

| Field | Type | Notes |
|---|---|---|
| `place` | Place | The searched place, for the headline, the map and the empty-state text |
| `currency` | string | `AUD` |
| `nearbyCount` | int | Vehicles in scope (SR-2) with no filters |
| `matchCount` | int | Vehicles that pass every filter. Equals search's `page.totalElements` |
| `price` | object \| null | `min`, `max`, `histogram` (14 ints): SR-15. `null` when `nearbyCount` is 0 |
| `brands` | `{ value, count }[]` | SR-14, SR-16 |
| `areas` | `{ value, count }[]` | SR-14, SR-16 |
| `ratings` | `{ minRating, count }[]` | SR-14, SR-17. `minRating: null` is "Any rating" |
| `relaxations` | `{ filter, value, matchCount }[]` | SR-19. Empty unless `matchCount` is 0 |

`relaxations[].filter` is one of `TYPE`, `PRICE`, `BRAND`, `MAX_DISTANCE`, `AREA`, `TRANSMISSION`, `MIN_SEATS`, `ENGINE_CC`, `MIN_RATING`. `value` is a string: the brand or area name, the enum value, or the number. It is `null` for `PRICE` and `ENGINE_CC`, which drop both bounds. The page writes the label ("Remove "Manual"") from its own filter state.

Example: Melbourne CBD, no filters.

`GET /api/v1/vehicles/search/facets?placeId=2`

```json
{
  "place": {
    "id": 2,
    "name": "Melbourne CBD",
    "label": "Melbourne CBD, VIC",
    "kind": "AREA",
    "city": "Melbourne",
    "lat": -37.8136,
    "lng": 144.9631,
    "timeZone": "Australia/Melbourne"
  },
  "currency": "AUD",
  "nearbyCount": 8,
  "matchCount": 8,
  "price": {
    "min": 35.00,
    "max": 140.00,
    "histogram": [2, 2, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1]
  },
  "brands": [
    { "value": "Honda", "count": 1 },
    { "value": "Kia", "count": 1 },
    { "value": "Mazda", "count": 1 },
    { "value": "Suzuki", "count": 1 },
    { "value": "Tesla", "count": 1 },
    { "value": "Toyota", "count": 1 },
    { "value": "Vespa", "count": 1 },
    { "value": "Yamaha", "count": 1 }
  ],
  "areas": [
    { "value": "Melbourne CBD", "count": 1 },
    { "value": "Southbank", "count": 1 },
    { "value": "Carlton", "count": 1 },
    { "value": "Docklands", "count": 1 },
    { "value": "Fitzroy", "count": 1 },
    { "value": "Richmond", "count": 1 },
    { "value": "St Kilda", "count": 1 },
    { "value": "Melbourne Airport", "count": 1 }
  ],
  "ratings": [
    { "minRating": null, "count": 8 },
    { "minRating": 4.0, "count": 8 },
    { "minRating": 4.5, "count": 4 },
    { "minRating": 4.8, "count": 3 }
  ],
  "relaxations": []
}
```

Example: the mockup's empty state. `GET /api/v1/vehicles/search/facets?placeId=2&transmission=MANUAL&maxPrice=50&minRating=4.5` returns the same `place` and `price` bounds. Every brand, area and histogram count is 0. The fields that change (excerpt):

```json
{
  "nearbyCount": 8,
  "matchCount": 0,
  "ratings": [
    { "minRating": null, "count": 1 },
    { "minRating": 4.0, "count": 1 },
    { "minRating": 4.5, "count": 0 },
    { "minRating": 4.8, "count": 0 }
  ],
  "relaxations": [
    { "filter": "TRANSMISSION", "value": "MANUAL", "matchCount": 2 },
    { "filter": "MIN_RATING", "value": "4.5", "matchCount": 1 }
  ]
}
```

The only manual car (Suzuki Swift, A$49, Laneway Motors 4.4) fails the rating filter. Without "Manual", two scooters under A$50 from Two Wheels Melbourne (4.9) match. Removing the price range still gives 0, so it is left out.

Errors: `400` for the same parameter problems as search.

Notes:

- The server works out `relaxations`, not the page. The facet counts cannot give them: removing "Cars" also clears seats and engine size, and removing one of several brands narrows the results instead of widening them. It is at most about ten counts on a one-city scope.

### 3. Compare

`GET /api/v1/vehicles/compare` · SRS 2.3 · Public

| Parameter | Type | Required | Allowed values | Default |
|---|---|---|---|---|
| `ids` | long list, comma-separated | yes | 1 to 3 different vehicle IDs | |
| `placeId` | long | no | An `id` from `GET /api/v1/places` | None: `distanceKm` is `null` |
| `startDate` | date | yes | As in search | |
| `endDate` | date | yes | As in search | |

The response holds the rows in the order of `ids`. It is not paged (3 at most).

`GET /api/v1/vehicles/compare?ids=1,3&placeId=2&startDate=2026-12-11&endDate=2026-12-14`

```json
{
  "items": [
    {
      "id": 1,
      "type": "CAR",
      "brand": "Toyota",
      "model": "Corolla Hybrid",
      "year": 2023,
      "bodyStyle": "SEDAN",
      "transmission": "AUTOMATIC",
      "seats": 5,
      "engineCc": null,
      "fuel": "HYBRID",
      "fuelDetail": "4.4 L / 100 km",
      "bags": 2,
      "helmets": null,
      "features": [],
      "pricePerDay": 68.00,
      "imageUrl": "/media/vehicles/1/1.jpg",
      "location": { "area": "Melbourne CBD", "lat": -37.8105, "lng": 144.9710 },
      "company": { "id": 1, "name": "Yarra Car Co.", "rating": 4.8, "reviewCount": 212 },
      "distanceKm": 0.8,
      "rentalDays": 3,
      "totalPrice": 204.00,
      "availability": { "status": "AVAILABLE", "unitsLeft": null, "bookedRanges": [] }
    },
    {
      "id": 3,
      "type": "CAR",
      "brand": "Mazda",
      "model": "CX-5",
      "year": 2022,
      "bodyStyle": "SUV",
      "transmission": "AUTOMATIC",
      "seats": 5,
      "engineCc": null,
      "fuel": "PETROL",
      "fuelDetail": null,
      "bags": 4,
      "helmets": null,
      "features": [],
      "pricePerDay": 94.00,
      "imageUrl": "/media/vehicles/3/1.jpg",
      "location": { "area": "Southbank", "lat": -37.8270, "lng": 144.9560 },
      "company": { "id": 2, "name": "Southbank Rentals", "rating": 4.6, "reviewCount": 148 },
      "distanceKm": 1.6,
      "rentalDays": 3,
      "totalPrice": 282.00,
      "availability": { "status": "FEW_LEFT", "unitsLeft": 2, "bookedRanges": [] }
    }
  ],
  "currency": "AUD"
}
```

Errors:

| Status | When |
|---|---|
| `400` | `ids` missing, more than 3, or repeated; unknown `placeId`; date problems as in search |
| `404` | An ID that does not exist or is out of search scope (not listed, or its company is not live). `detail` names the ID |

Notes:

- This page uses it to refill the compare tray after a reload (`?compare=1,3`). Otherwise the tray uses rows the page already has.
- The compare page (no mockup yet) uses the same call. It may need more fields once it has a mockup.

### 4. Place suggestions

`GET /api/v1/places` · SRS 2.3 · Public

Used by this page's Where field and the landing page's "Pick-up location" field ("City, district or airport").

| Parameter | Type | Required | Allowed values | Default |
|---|---|---|---|---|
| `q` | string | no | Up to 100 characters, as landing rule LP-5 | Empty: every `CITY` place, A to Z |
| `size` | int | no | 1 to 20 | 8 |

`GET /api/v1/places?q=mel`

```json
{
  "content": [
    { "id": 1, "name": "Melbourne", "label": "Melbourne, VIC", "kind": "CITY", "city": "Melbourne", "lat": -37.8136, "lng": 144.9631, "timeZone": "Australia/Melbourne" },
    { "id": 3, "name": "Melbourne Airport", "label": "Melbourne Airport, VIC", "kind": "AIRPORT", "city": "Melbourne", "lat": -37.6690, "lng": 144.8410, "timeZone": "Australia/Melbourne" },
    { "id": 2, "name": "Melbourne CBD", "label": "Melbourne CBD, VIC", "kind": "AREA", "city": "Melbourne", "lat": -37.8136, "lng": 144.9631, "timeZone": "Australia/Melbourne" }
  ],
  "page": { "size": 8, "number": 0, "totalElements": 3, "totalPages": 1 }
}
```

Errors: `400` when `q` is over 100 characters or `size` is out of range.

Notes:

- Matching: `q` is found anywhere in `label` or in the place's other names, ignoring case and accents ("ben thanh" finds "Bến Thành"). Places whose `name` starts with `q` come first, then A to Z by `name`.
- Other names (assumption): each place stores a hidden list such as `Saigon`, `HCMC` for Ho Chi Minh City places. They are searched but not returned. The mockup already treats "Saigon" as Ho Chi Minh City.
- Places come from a `Place` table that the team seeds: the cities, suburbs or districts, and airports where companies list vehicles (assumption, open question 7).

### 4b. One place

`GET /api/v1/places/{id}` · SRS 2.3 · Public

Returns one Place. The search page calls it when it opens with `placeId` in its URL, to fill the Where field and the headline. The vehicle page calls it for "0.8 km from Melbourne CBD" and the "Your search" marker.

`GET /api/v1/places/2`

```json
{ "id": 2, "name": "Melbourne CBD", "label": "Melbourne CBD, VIC", "kind": "AREA", "city": "Melbourne", "lat": -37.8136, "lng": 144.9631, "timeZone": "Australia/Melbourne" }
```

Errors: `404` when no place has this `id`.

### 5. Active booking count (nav)

`GET /api/v1/bookings/summary` · SRS 2.4 · `CUSTOMER`

No parameters. Counts the logged-in customer's bookings whose status is `REQUESTED`, `APPROVED` or `PICKED_UP`.

```json
{ "activeCount": 2 }
```

Errors:

| Status | When |
|---|---|
| `401` | Not logged in. The page does not call it for visitors |
| `403` | Role is `COMPANY` or `ADMIN` |

Notes:

- It sits under `/bookings`, next to vehicle.md's `POST /api/v1/bookings` and the future "My bookings" list. Every customer page calls it along with `GET /api/v1/auth/me`.

## Endpoints used from other pages

| Endpoint | Defined in | Used for |
|---|---|---|
| `GET /api/v1/auth/me` | login.md | Nav first name, initials, account menu name, email and role label. A `401` means logged out |
| `POST /api/v1/auth/logout` | login.md | Log out in the account menu. `204`, then the page opens the login page |
| `GET /api/v1/vehicles/{id}`, the vehicle's availability calendar and its price quote | vehicle.md | Not called here. The View button opens `../vehicle/index.html?id={id}&from={from}&to={to}&placeId={placeId}` and that page loads them. A search row's `availability` and `totalPrice` must give the same answer for the same dates (SR-5 to SR-8) |

## Validation and business rules

Numbered so the SRS can pick them up. "Page" marks a rule for the frontend only.

### Place and scope

**SR-1.** A search needs a place and both dates. Picking a suggestion sets the place. On submit with typed text, or with `location` from the landing page, the page calls `GET /api/v1/places?q=<text>`. It uses the place whose `label` equals the text (ignoring case), or else the first suggestion. If there are no suggestions, the Where field shows its error state ("No place matches"), and no search is sent.

**SR-2.** A vehicle is in scope when `listed` is `true`, its company is live, meaning `verified` with an `ACTIVE` account (login.md LOGIN-26, LOGIN-27), and its `location.city` equals the place's `city`, ignoring case. Vehicles out of scope never appear and are not counted anywhere on the page.

**SR-3.** `distanceKm` is the straight-line distance (haversine, Earth radius 6371 km) from the place's `lat`/`lng` to the vehicle's pick-up `lat`/`lng`, rounded half-up to 1 decimal place. Filters and sorts use the rounded value. Example: Melbourne CBD (−37.8136, 144.9631) to Richmond (−37.8230, 145.0000) is 3.4 km.

### Dates and price

**SR-4.** `startDate` is after today, and `endDate` is after `startDate`. The earliest pick-up is tomorrow, because every booking waits for the company to approve it (README, cross-page decision 2). "Today" is the date in the searched place's `timeZone`. Page: the return picker cannot go before pick-up. If the customer picks a return date on or before the pick-up date, the page moves it to the day after pick-up.

**SR-5.** `rentalDays` is the number of days from `startDate` to `endDate` (11 Dec to 14 Dec is 3). `totalPrice` = `pricePerDay` × `rentalDays`, to 2 decimal places. Example: 68.00 × 3 = 204.00. The page labels it "est.": it comes before any company fees. The amount the customer pays is the booking's `totalPrice` (fee rule, SRS 2.8; quote in vehicle.md).

### Availability

**SR-6.** A booking blocks its vehicle when its status is `REQUESTED`, `APPROVED` or `PICKED_UP` (proposal, open question 2). `REJECTED`, `CANCELLED` and `RETURNED` never block.

**SR-7.** A blocking booking clashes with the searched dates when `booking.startDate <= endDate` and `booking.endDate >= startDate`. Both ends count, so the return day is not free for a new pick-up: a booking from 11 to 12 Dec clashes with a search from 12 to 14 Dec. This matches the vehicle page's calendar (VEH-6, VEH-7; README, cross-page decision 3).

**SR-8.** `availability.status`:

| Status | When | Page shows |
|---|---|---|
| `BOOKED` | At least one blocking booking clashes. With option A: every unit is taken on at least one day | "Booked 11–12 Dec" from `bookedRanges`: the clashing bookings' dates, sorted by `startDate`, with ranges that overlap or touch merged |
| `FEW_LEFT` | Option A only. `unitsLeft` is 1 or 2 and less than `units`. `unitsLeft` = `units` minus the largest number of clashing blocking bookings on any one day | "Only 2 left" |
| `AVAILABLE` | Otherwise | "Free for your dates" |

**SR-9.** Availability never removes a vehicle from the results. Booked vehicles still appear (muted row, outlined map pin) and count in every number on the page.

### Filters

**SR-10.** Filters in different groups combine with AND. Several brands, or several areas, combine with OR. A filter that is not sent does not apply.

| Parameter | A vehicle passes when |
|---|---|
| `type` | `type` equals it |
| `minPrice`, `maxPrice` | `minPrice ≤ pricePerDay ≤ maxPrice` |
| `brand` | `brand` equals one of the values, ignoring case |
| `maxDistanceKm` | `distanceKm ≤ maxDistanceKm` |
| `area` | `location.area` equals one of the values, ignoring case |
| `transmission` | `transmission` equals it |
| `minSeats` | It is a motorbike, or `seats ≥ minSeats` |
| `minEngineCc`, `maxEngineCc` | It is a car, or `minEngineCc ≤ engineCc ≤ maxEngineCc` |
| `minRating` | The company's `rating` (1 decimal place) is at least `minRating`. A company with no rating fails |

**SR-11.** Page: changing Type clears seats and engine size. Seats show only for Cars: Any, 4+, 5+, 7+. Engine size shows only for Motorbikes: Any, "≤ 125 cc" (sends `maxEngineCc=125`) and "126–160 cc" (sends `minEngineCc=126&maxEngineCc=160`). With All, the group says "Choose cars or motorbikes first".

**SR-12.** Page: the price slider runs from `price.min` to `price.max`. A thumb at its end sends no parameter, so the top end means "and above" ("A$140+"). The two thumbs stay at least one step apart (mockup step: A$5 in Melbourne, A$1 in Ho Chi Minh City). Results reload when a thumb is let go, not while it is dragged.

**SR-13.** Page: each active filter shows as a removable tag, with one tag per brand and per area. "Clear all" resets every filter. The place, dates, sort, view and compare tray stay.

### Facets

**SR-14.** Each count applies every active filter except its own group's. The groups are price, brand, area and rating. `maxDistanceKm` and `area` are separate groups. Example in Melbourne CBD with `type=MOTORBIKE`: brands are Honda 1, Vespa 1, Yamaha 1 and the other five 0. Adding `brand=Honda` leaves the brand counts the same, but the area counts drop to Carlton 1 and 0 for the rest.

**SR-15.** Price bounds ignore every filter. `min` is the lowest `pricePerDay` in scope, rounded down to a multiple of 5. `max` is the highest, rounded up to a multiple of 5. If they are equal, `max` = `min` + 5. The histogram has 14 equal bins from `min` to `max`. A vehicle goes in bin `floor((pricePerDay − min) / (max − min) × 14)`, at most 13. Bins count vehicles that pass every filter except price. Melbourne: bounds 35 and 140, histogram `[2, 2, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1]`.

**SR-16.** Brand options: every brand in scope, A to Z. Area options: every area in scope, nearest first, where an area's distance is that of its nearest vehicle; ties A to Z. Options with count 0 are still listed. Page: an option with count 0 that is not ticked is disabled.

**SR-17.** Rating options are fixed: Any rating, 4.0 and up, 4.5 and up, 4.8 and up. Only one can be chosen.

### Sort

**SR-18.** Sort orders. The "Company rating" sort puts companies with no rating last.

| `sort` | Menu label | Order | Ties |
|---|---|---|---|
| `recommended` | Recommended | `BOOKED` last. Then score = company rating (3.0 if none) − 0.1 × `distanceKm`, high to low | `pricePerDay` low to high, then `id` |
| `price,asc` | Price: low to high | `pricePerDay` low to high | `distanceKm`, then `id` |
| `price,desc` | Price: high to low | `pricePerDay` high to low | `distanceKm`, then `id` |
| `rating,desc` | Company rating | Company rating high to low | `distanceKm`, then `id` |
| `distance,asc` | Distance | `distanceKm` near to far | `id` |

Recommended in Melbourne CBD, no filters, 11–14 Dec: Corolla Hybrid (4.72), PCX 160 (4.69), CX-5 (4.44), Primavera 150 (4.28), NMAX 155 (4.16), Swift (4.11), Carnival (2.25), then Model 3 (booked). The formula and the 3.0 default are proposals (open question 4).

### Empty state

**SR-19.** When a search returns 0 results, the page shows the empty state instead of the list or map, and the List / Map toggle is disabled. "Loosen one filter" lists `relaxations`, with one entry per active filter tag (each brand and each area on its own). An entry's `matchCount` is the number of results with only that tag removed. Removing Type also removes seats and engine size. Entries with `matchCount` 0 are left out. Order: `matchCount` high to low, with ties in tag order (type, price, brand, distance, area, transmission, seats, engine size, rating). The last line is always "Clear all filters" with `nearbyCount`. Example (Melbourne CBD, Manual, up to A$50, rated 4.5+): Remove "Manual" +2, Remove "Rated 4.5+" +1, Clear all filters +8. If `nearbyCount` is 0, the page says no vehicles are listed near the place yet and shows no suggestions (no mockup; assumption).

### Compare

**SR-20.** Page: a customer can tick up to 3 vehicles. With 3 ticked, the other Compare boxes are disabled with the hint "You can compare up to 3". The tray appears at 2 ticks and shows "+ Add a third" while there are fewer than 3. Its Compare link carries the IDs, dates and place. Searching a place in another city clears the tray and every filter. Changing dates, sort or filters keeps the tray.

### Map

**SR-21.** Page: the map shows one pin per result (up to 100) at the vehicle's pick-up point, labelled with the price per day. `BOOKED` pins are outlined. Rings mark 2, 5 and 10 km around the place. The first result is picked when the map opens. If the picked vehicle leaves the results, the first result is picked again.

### Paging

**SR-22.** The list view loads 20 rows a page. The map view loads up to 100 in one call. A `size` above 100 is rejected with `400`.

### Nav

**SR-23.** Page: the nav shows the first word of `fullName`. The initials are the first letters of the first and last words, in capitals ("Minh Tran" gives "MT"). `role` `CUSTOMER` shows as "Customer account".

**SR-24.** Page: "My bookings" shows `activeCount` as 2 digits ("02") and hides the number when it is 0 (assumption). Active means `REQUESTED`, `APPROVED` or `PICKED_UP`.

## Changes to shared models

Merged into the README on 2026-11-06, except `Vehicle.units`, which waits for README decision 4. Kept here as the reason for each change.

| Model | Change | Why |
|---|---|---|
| Place (new) | Add Place as a shared model. It also stores hidden other names (for example `Saigon`) that matching uses but responses leave out | Search and landing both use it. The vehicle form can use `CITY` places to fill `Location.city` |
| Location | `city` must be the `city` of a `CITY` place, chosen from a list in the vehicle form, not typed | SR-2 matches the city as text. Typed values such as "HCMC" and "Ho Chi Minh City" would hide vehicles from search |
| Vehicle | Add `units` (int, 1 or more, default 1): how many identical vehicles the listing has. Only if open question 1 picks option A | "Only N left" (SR-8) |

## Open questions

1. **"Only N left" when one Vehicle row is one physical vehicle.** The README's Vehicle is one physical vehicle, so "Only 2 left" has no meaning yet. Option A: add `Vehicle.units`. A booking takes one unit, and availability counts free units for each day (SR-8). Option B: keep the README model and drop `FEW_LEFT` and `unitsLeft`. The label leaves the page, and a company adds each identical vehicle as its own row. This file shows A because the mockup does. B is simpler and is enough for the brief. The choice also changes vehicle.md's availability calendar and booking check.
2. **Do `REQUESTED` bookings block dates (SR-6)?** Proposal: yes. Two customers cannot request the same vehicle for the same days, and an approval can never clash. The cost is that an unanswered request holds the vehicle, so requests may need to expire. Also: can a vehicle returned on a day be picked up the same day (SR-7)? This must match vehicle.md's calendar and its `409` on `POST /api/v1/bookings`.
3. **Booked vehicles in results.** The mockup shows them, flagged (SR-9). Keep that, hide them, or add a "Free for my dates only" filter?
4. **Recommended sort.** Accept the formula in SR-18, or pick something simpler? It could later grow into the "Personalised recommendations" custom feature.
5. **Search scope.** Resolved 2026-11-06: only vehicles of live companies, meaning verified with an `ACTIVE` account (SR-2). A suspended company's vehicles leave search through its account's status, so Company needs no status of its own (login.md LOGIN-26, LOGIN-27).
6. **Logged-out visitors.** Can they open the search page? The API allows it. They would need a logged-out nav, which has no mockup.
7. **Where places come from.** A seeded `Place` table (proposal) or an external geocoder such as Nominatim or Google Places (licence, API key and rate limits go in SRS §7)? "Near me" from the browser's location would need `lat` and `lng` parameters. It is not in the mockup.
8. **Engine sizes over 160 cc.** These motorbikes match neither engine option. Add "Over 160 cc", or build the options from the data?
9. **Real map.** The mockup draws a stylised SVG. The real page needs a map library and tiles (for example Leaflet with OpenStreetMap), which go in SRS §7.
10. **List paging.** Use "Show more" (assumed in SR-22) or numbered pages? The mockup shows neither.
11. **Dates and defaults.** The server takes "today" from the place's `timeZone` (SR-4), while landing rule LP-2 picks default dates in the visitor's own time zone. The two can differ by a day near midnight; is that acceptable? Also: is Melbourne CBD the right default place when the landing page sends no `location`, or should the page use the customer's last search?
