# Landing page

The public home page. It explains RentXe, starts a vehicle search, and points rental companies to sign-up.

| | |
|---|---|
| Mockup | `assets/mockups/landing-3d/index.html` |
| Route | `/` (assumption) |
| Access | Public |

Most of the page is static marketing copy. It needs one endpoint of its own (featured reviews) and two from other files.

## URL parameters and states

| Parameter or state | Values | What it does | In the product? |
|---|---|---|---|
| `?vehicle=` | `car`, `bike` | Starts the hero form on the Car or Motorbike tab, with the matching 3D vehicle or photo. Default `car`. | Optional. Nothing links to it yet. |
| `?mode=` | `static`, `3d` | Forces the phone layout (a photo) or the desktop layout (3D scene with scroll zoom). | No. A test switch. The product picks the layout from the screen size. |
| `?scenery=`, `?time=`, `?camera=`, `?car=` | | Settings for the "Prototype controls" panel. | No. Mockup tooling. |
| Logged out | | Header shows **Log in** and **Sign up**. | Yes. The only state the mockup shows. |
| Logged in | | Not in the mockup. See open question 5. | To decide |
| Reduced motion | | No scroll zoom. About becomes a normal section. | Yes. No API impact. |

## What the page shows

"Static" means the content is fixed in the page and needs no API.

| Area | Element | Data source |
|---|---|---|
| Header | Logo and "RentXe" | Static. Links to the top of the page. |
| Header | About, How it works, For rental companies, Reviews | Static. In-page links. |
| Header | Log in | Static link to `/login` |
| Header | Sign up | Static link to `/login?view=signup` |
| Header | Logged-in nav (not in mockup) | `GET /api/v1/auth/me` (login.md). Assumption. |
| Hero | 3D scene (desktop) or photo (phones) | Static assets. Follows the Car or Motorbike tab. |
| Hero | Eyebrow "New · Cars & motorbikes from local rental companies" | Static |
| Hero | Heading "Find your ride. Hit the road." and lead text | Static |
| Hero form | Car / Motorbike tabs | Static. Fixed values `CAR`, `MOTORBIKE` (Vehicle `type`). |
| Hero form | Pick-up location box | Visitor input. Suggestions from search.md (assumption). |
| Hero form | Pick-up date, Return date | Visitor input. Defaults set in the browser (LP-2). |
| Hero form | Search button | Opens the search page with query parameters. No API call. See [Hand-off to the search page](#hand-off-to-the-search-page). |
| Hero | Trust line: "Verified rental companies", "Compare prices side by side", "Reviews from real renters" | Static. Each claim is a rule the system must keep (LP-12, LP-13). |
| Zoom | Vehicle screen splash "(01) ABOUT" | Static |
| (01) About | Statement, "For renters", "For rental companies", "How it works" link | Static |
| (02) How it works | Four steps: Search, Compare, Request, Ride & return | Static |
| (03) For rental companies | Heading and four bullets | Static |
| (03) For rental companies | Register your company | Static link to `/login?view=signup&as=company` |
| (03) For rental companies | See how it works | Static. `href="#"` in the mockup, a dead link. |
| (03) For rental companies | "Booking requests" card (Honda Vision, Toyota Vios, Yamaha NVX) | Static illustration of the company dashboard. Not live data. No API. |
| (04) Reviews | Heading and intro text | Static |
| (04) Reviews | Three review cards: stars | `GET /api/v1/reviews/featured` → `rating` |
| (04) Reviews | Quote | → `comment` |
| (04) Reviews | Name "Minh T." | → `authorDisplayName` |
| (04) Reviews | "rented a motorbike for 3 days" | → `vehicleType` and `rentalDays` |
| (04) Reviews | Third card "Khanh N. · rental company owner" | Cannot come from a Review. See open question 1. |
| CTA | "Ready to ride?" text | Static |
| CTA | Search vehicles | Static. Scrolls to the hero form. |
| CTA | List your fleet | Static. Scrolls to "For rental companies". |
| Footer | Logo and tagline | Static |
| Footer | About, How it works, Reviews, List your fleet | Static. In-page links. |
| Footer | Company log in | Static link to `/login?as=company` |
| Footer | Contact us, Terms, Privacy | Static. `href="#"` in the mockup. No pages designed yet. |
| Footer | "© 2026 RentXe · ... placeholder content" | Static. Remove "prototype" and "placeholder" before release. |
| Mockup only | Toast "Prototype: this would open the search results page" | None. The product opens the search page. |
| Mockup only | "Prototype controls" panel | None. Mockup tooling. |

## Endpoints

### GET /api/v1/reviews/featured

Reviews for the "Rated by the people who rode" cards.

| | |
|---|---|
| SRS area | 2.6 Reviews and ratings |
| Access | Public |
| Used by | Landing page, (04) Reviews. The page asks for `?page=0&size=3`. |

Query parameters:

| Name | Type | Required | Rules |
|---|---|---|---|
| `page` | int | No | Default `0`. At least `0`. |
| `size` | int | No | Default `3`. `1` to `10`. |

There is no `sort`. The server orders newest first (LP-8). A `sort` parameter is ignored.

Response `200`, a standard page. Each item is a read-only view of a Review:

| Field | Type | Source |
|---|---|---|
| `id` | long | Review `id` |
| `rating` | int | Review `rating`, 1 to 5 |
| `comment` | string | Review `comment` |
| `authorDisplayName` | string | _derived_ from the author's `fullName`: first name and last initial (LP-9) |
| `vehicleType` | enum | _derived_: Vehicle `type` of the booked vehicle |
| `rentalDays` | int | _derived_: booking `endDate` minus `startDate`, in days (LP-10) |

```json
{
  "content": [
    {
      "id": 412,
      "rating": 5,
      "comment": "Found a scooter two streets from my hotel, booked it in a few minutes and picked it up the same afternoon.",
      "authorDisplayName": "Minh T.",
      "vehicleType": "MOTORBIKE",
      "rentalDays": 3
    },
    {
      "id": 397,
      "rating": 5,
      "comment": "Comparing three companies on one page saved us a lot of calls. The car was exactly as listed.",
      "authorDisplayName": "Sarah L.",
      "vehicleType": "CAR",
      "rentalDays": 7
    },
    {
      "id": 381,
      "rating": 4,
      "comment": "Easy pick-up at the airport. The car was clean and the return took two minutes.",
      "authorDisplayName": "Anh L.",
      "vehicleType": "CAR",
      "rentalDays": 5
    }
  ],
  "page": { "size": 3, "number": 0, "totalElements": 37, "totalPages": 13 }
}
```

The first two items are the mockup's cards. The third is made up, based on the Toyota Vios request in the company card. The mockup's third card is a company owner's quote, which this endpoint cannot return (open question 1).

Errors:

| Status | When |
|---|---|
| `400` | `page` or `size` out of range, or not a number |

```json
{
  "type": "about:blank",
  "title": "Bad Request",
  "status": 400,
  "detail": "Validation failed",
  "instance": "/api/v1/reviews/featured",
  "errors": [{ "field": "size", "message": "must be between 1 and 10" }]
}
```

Notes:

- Read-only. No `401` or `403`: anyone can call it.
- An empty `content` is a valid answer, for example on a new site with no reviews.
- Never returns the author's id, full name or email.
- Which reviews are eligible: LP-7.
- The answer is the same for every visitor, so the server may cache it for a few minutes (assumption).

## Endpoints used from other pages

The landing page calls these. Their schemas live in the owning file.

| Method and path | Owner | What the landing page uses it for |
|---|---|---|
| `GET /api/v1/auth/me` | login.md | On load. `401` means logged out: show **Log in** and **Sign up**. `200` means logged in: show the nav for the user's `role`, with their `fullName`. Assumption: the mockup shows only the logged-out header. The customer nav and its data (for example the "My bookings" count) are defined by search.md. |
| `GET /api/v1/places?q=` | search.md | Suggestions under the **Pick-up location** box as the visitor types, the same as the search page's **Where** box. Assumption: the landing mockup shows a plain text box. |

The landing page does not call the vehicle search endpoint. It opens the search page, and the search page calls it.

### Hand-off to the search page

Submitting the hero form opens the search page. It makes no API call.

```
/search?type=MOTORBIKE&location=District%201%2C%20Ho%20Chi%20Minh%20City&from=2026-12-11&to=2026-12-14
```

| Parameter | Type | Sent | Value |
|---|---|---|---|
| `type` | enum `CAR`, `MOTORBIKE` | Always | The selected tab |
| `location` | string, URL-encoded | Only when the box is not blank | The trimmed text, or the label of the chosen suggestion |
| `from` | date | Always | Pick-up date, `YYYY-MM-DD` |
| `to` | date | Always | Return date, `YYYY-MM-DD` |

- No paging, sort or filter parameters are sent. The search page starts with its defaults.
- `from` and `to` match the links the search mockup already builds (`#vehicle?id=…&from=…&to=…`, `#compare?ids=…&from=…&to=…`).
- search.md reads all four. It turns `location` into a place (search.md SR-1). The search mockup itself does not read `type` or `location` yet; it reads only the prototype switches `?city=` and `?view=`.

### Other page links (no API)

| Link | Goes to |
|---|---|
| Log in | `/login` |
| Sign up | `/login?view=signup` |
| Register your company | `/login?view=signup&as=company` |
| Company log in | `/login?as=company` |

## Validation and business rules

Hero search form:

| ID | Rule |
|---|---|
| LP-1 | Vehicle type is `CAR` or `MOTORBIKE`. Default `CAR`. `?vehicle=bike` on the landing URL starts on `MOTORBIKE`. |
| LP-2 | The pick-up date defaults to tomorrow and the return date to three days after it, in the visitor's local time zone. |
| LP-3 | The pick-up date must be after today: the earliest pick-up is tomorrow, because every booking waits for the company to approve it. Same rule as search.md SR-4 and vehicle.md VEH-3 (README, cross-page decision 2). |
| LP-4 | The return date must be after the pick-up date. If the visitor picks a return date on or before the pick-up date, the form moves it to the day after pick-up, as the search page does. |
| LP-5 | Pick-up location is optional free text, trimmed, at most 100 characters (assumption). If blank, `location` is not sent and the search page uses its default city. |
| LP-6 | Submitting opens the search page with the parameters above. The search page must check them again, because anyone can edit a URL. |

Featured reviews:

| ID | Rule |
|---|---|
| LP-7 | A review is eligible when all of these hold: `rating` is 4 or 5; `comment` is not blank and at most 200 characters; the author's `status` is `ACTIVE`; the company is `verified`. Assumption, see open question 2. |
| LP-8 | Eligible reviews are shown newest first. |
| LP-9 | The author is shown as first name and last initial only: the first word of `fullName`, a space, the first letter of the last word, and a full stop (`Minh Tran` → `Minh T.`). A one-word name is shown as is. The full name, email and id are never shown. |
| LP-10 | `rentalDays` counts days the same way as the fee rule in SRS §2.8 (return date minus pick-up date). The card shows "for 1 day", "for N days", or "for a week" when it is 7. |
| LP-11 | If the call fails or returns no reviews, the page still loads. The cards are hidden; the section heading and text stay, so the **Reviews** nav link still works. Assumption. |

Promises in the page copy. Other files own these rules; they are listed so the SRS matches what the page says.

| ID | Copy | Rule |
|---|---|---|
| LP-12 | "Verified rental companies" | Search shows only vehicles from companies with `verified = true`. |
| LP-13 | "Reviews from real renters" | Only the customer of a `RETURNED` booking can review it, once. |
| LP-14 | "The rental company approves it" and "Every booking, tracked in one place" | A new booking starts as `REQUESTED`. The company approves or rejects it. The customer sees all their bookings and their status in one list. |
| LP-15 | "The fee is worked out from your rental period" | `Booking.totalPrice` is derived from the dates by the fee rule in SRS §2.8. |
| LP-16 | "Record every pick-up, return and vehicle condition" | Companies record pick-up and return with condition notes (SRS §2.5). The README Booking has no field for these notes yet. |

## Changes to shared models

None needed for this page as written.

`authorDisplayName` and `rentalDays` are worked out when the response is built. They are not stored, so they do not belong in the Review model.

Changes only if the team picks that answer to an open question:

| Model | Change | When |
|---|---|---|
| Review | Add `featured` (boolean, set by an admin, default `false`) | Admins pick the landing reviews (open question 2) |
| Review | Replace `rating` with `vehicleRating` and `companyRating` (int, 1 to 5) | Customers rate the vehicle and the company separately (open question 3) |
| Company | Add a cancellation rule field | Each company sets its own cancel rule (open question 4) |

## Open questions

1. The third review card is a rental company owner's quote. A Review can only come from a customer's returned booking. Show three customer reviews (this file assumes so), move owner quotes into the "For rental companies" section as static copy, or add a testimonial feature (not in any mockup)?
2. Are featured reviews picked automatically (LP-7, assumed here) or by an admin? Admin picks need `Review.featured` and an admin screen that no mockup shows.
3. The reviews intro says customers "rate the vehicle and the company". The README Review has one `rating`. Keep one rating and change the copy, or store two ratings?
4. "You can cancel where their rules allow" (How it works, step 3) says each company sets its own cancel rule. Is it one rule for everyone in SRS §2.8, or one per company? Change the copy to match.
5. What does a logged-in visitor see on `/`? The landing page with their role's nav, or a redirect (customer to search, company to their dashboard, admin to the admin area)?
6. Resolved: search.md defines `GET /api/v1/places` and reads `type`, `location`, `from` and `to` from its URL.
7. Can a rental start today? The first review ("picked it up the same afternoon") says yes, but LP-3 follows the vehicle page's date fields, where the earliest pick-up is tomorrow. If same-day pick-up is wanted, change LP-3, SR-4 and VEH-3 together, or change the review copy.
8. "See how it works" in the companies section, and Contact us, Terms and Privacy in the footer, link nowhere. Are Terms and Privacy pages in scope? The sign-up form links to them too.
