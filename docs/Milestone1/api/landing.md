# Landing page

The public home page. It explains RentXe, starts a vehicle search, and points rental companies to sign-up.

| | |
|---|---|
| Mockup | `assets/mockups/landing-3d/index.html` |
| Route | `/` (assumption) |
| Access | Public |

Most of the page is static marketing copy, the reviews included. It has no endpoint of its own and calls two from other files.

## URL parameters and states

| Parameter or state | Values | What it does | In the product? |
|---|---|---|---|
| `?vehicle=` | `car`, `bike` | Starts the hero form on the Car or Motorbike tab, with the matching 3D vehicle or photo. Default `car`. | Optional. Nothing links to it yet. |
| `?mode=` | `static`, `3d` | Forces the phone layout (a photo) or the desktop layout (3D scene with scroll zoom). | No. A test switch. The product picks the layout from the screen size. |
| `?scenery=`, `?time=`, `?camera=` | `mountains`, `city`; `day`, `sunset`, `night`; `scenic`, `chase`, `topdown` | Pins one part of the hero scene, for screenshots and demos. Without them the page picks (LP-17 to LP-20). | Yes, as a test switch. |
| `?car=` | hex colour | Body colour of the 3D vehicle. | No. Mockup tooling. |
| `?user=` | `customer`, `company`, `admin` | Previews the logged-in header (LP-24) with sample users. Also in the panel's User row. | No. The product reads `GET /api/v1/auth/me`. |
| Logged out | | Header shows **Log in** and **Sign up**. | Yes. The only state the mockup shows. |
| Logged in | | Same page. **Log in** and **Sign up** become the account menu (LP-24). No redirect. Not in the mockup yet. | Yes |
| Reduced motion | | No scroll zoom. About becomes a normal section. | Yes. No API impact. |

## What the page shows

"Static" means the content is fixed in the page and needs no API.

| Area | Element | Data source |
|---|---|---|
| Header | Logo and "RentXe" | Static. Links to the top of the page. |
| Header | About, How it works, For rental companies, Reviews | Static. In-page links. |
| Header | Log in | Static link to `/login` |
| Header | Sign up | Static link to `/login?view=signup` |
| Header | Theme toggle, next to Log in: one button that cycles System, Light, Dark | Browser only: `localStorage` (LP-23). No API. |
| Header | Account menu when logged in (mockup: `?user=`) | `GET /api/v1/auth/me` (login.md): initials, first name, `role` (LP-24) |
| Hero | 3D scene (desktop) or photo (phones) | Static assets. Follows the Car or Motorbike tab. Scenery, camera and time of day are picked in the browser on each load (LP-17 to LP-21). No API. |
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
| (03) For rental companies | See how it works | Static link to `/for-companies`, a static page (LP-25). A dead link (`href="#"`) in the mockup. |
| (03) For rental companies | "Booking requests" card (Honda Vision, Toyota Vios, Yamaha NVX) | Static illustration of the company dashboard. Not live data. No API. |
| (04) Reviews | Heading and intro text | Static |
| (04) Reviews | Three review cards: stars, quote, name, "rented a motorbike for 3 days" | Static sample content written into the page (LP-21). No API. |
| (04) Reviews | Third card "Khanh N. · rental company owner" | Static. It can stay, because the cards are no longer real Review rows. |
| CTA | "Ready to ride?" text | Static |
| CTA | Search vehicles | Static. Scrolls to the hero form. |
| CTA | List your fleet | Static. Scrolls to "For rental companies". |
| Footer | Logo and tagline | Static |
| Footer | About, How it works, Reviews, List your fleet | Static. In-page links. |
| Footer | Company log in | Static link to `/login?as=company` |
| Footer | Contact us | Static email link: `mailto:support@rentxe.example` (address to be chosen). A dead link in the mockup. |
| Footer | Terms, Privacy | Static links to `/terms` and `/privacy`, plain text pages (LP-25). Dead links in the mockup. |
| Footer | "© 2026 RentXe · ... placeholder content" | Static. Remove "prototype" and "placeholder" before release. |
| Mockup only | Toast "Prototype: this would open the search results page" | None. The product opens the search page. |
| Mockup only | Toast "Prototype: the … page comes later" | None. Links to pages with no mockup yet: `/for-companies`, `/terms`, `/privacy` and the account pages. |
| Mockup only | "Prototype controls" panel | None. Mockup tooling. |

## Endpoints

None in the MVP. The reviews section is static (LP-21), so the landing page needs no endpoint of its own.

### Option for later: GET /api/v1/reviews/featured

Not in the MVP. Kept here in case the team later wants real reviews on the landing page. If it is built, LP-7 to LP-11 apply, and the page hides the section when the call gives nothing to show (LP-11).

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
- An empty `content` is a valid answer, for example on a new site with no reviews. The endpoint never answers `404` for "no reviews"; the page treats an empty list like a failed call (LP-11).
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
| See how it works | `/for-companies` (static page) |
| Terms | `/terms` (static page) |
| Privacy | `/privacy` (static page) |
| Contact us | `mailto:support@rentxe.example` |

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

Hero scene (desktop 3D only):

| ID | Rule |
|---|---|
| LP-17 | Scenery: each page load picks Mountains or City at random, with equal chances. |
| LP-18 | Camera: each page load picks Scenic, Chase or Top at random, with equal chances. The Front ¾ and Side cameras are removed. |
| LP-19 | Time of day comes from the visitor's local clock: Day from 07:00 to 16:59, Sunset from 05:00 to 06:59 and from 17:00 to 19:59, Night from 20:00 to 04:59. The light or dark theme never changes it (LP-22). |
| LP-20 | `?scenery=`, `?camera=` and `?time=` pin that part of the scene. The page never writes them back to the URL, so a plain reload picks again. |

Phones and touch tablets show the static photo instead of the 3D scene, so LP-17 to LP-20 do not apply there.

Theme:

| ID | Rule |
|---|---|
| LP-22 | The page follows the site's light or dark theme: header, sections, cards and footer. The hero scene does not: its sky comes only from LP-19, so a dark-theme visitor at noon sees Day, and a light-theme visitor at 21:00 sees Night. The copy over the hero stays white on the scene, and the hero search box stays light, in both themes. |
| LP-23 | The theme starts from the visitor's system setting (`prefers-color-scheme`). A theme toggle in the header, next to **Log in**, offers System, Light and Dark. The choice is saved in the browser's `localStorage` (README, Theme), so it holds on every page and after a reload. No API call. |

Header:

| ID | Rule |
|---|---|
| LP-24 | Logged out, the header shows the theme toggle, **Log in** and **Sign up**. Logged in, the page stays the same and nothing redirects: **Log in** and **Sign up** are replaced by the account menu, with the visitor's initials and first name from `GET /api/v1/auth/me`. A customer gets the same menu as the search page (search.md). A company's menu adds **Dashboard**, and an admin's adds **Admin** (assumption until those pages are mocked up). Every menu has **Log out**. |

Static pages linked from here:

| ID | Rule |
|---|---|
| LP-25 | `/for-companies`, `/terms` and `/privacy` are static pages with no API. `/for-companies` explains the company side in six steps: register; get verified by an admin (listings appear in search only after that); list vehicles; approve or decline requests; record pick-up, return and condition; build a rating from finished rentals. It ends with **Register your company** (`/login?view=signup&as=company`). `/terms` and `/privacy` hold placeholder text until the team writes them. Each page needs a simple wireframe. |

Reviews section:

| ID | Rule |
|---|---|
| LP-21 | The reviews section shows three fixed sample reviews written into the page. It makes no API call, so it always shows. |

Featured reviews from the API (only if the option above is built):

| ID | Rule |
|---|---|
| LP-7 | A review is eligible when all of these hold: `rating` is 4 or 5; `comment` is not blank and at most 200 characters; the author's `status` is `ACTIVE`; the company is `verified`. Assumption, see open question 2. |
| LP-8 | Eligible reviews are shown newest first. |
| LP-9 | The author is shown as first name and last initial only: the first word of `fullName`, a space, the first letter of the last word, and a full stop (`Minh Tran` → `Minh T.`). A one-word name is shown as is. The full name, email and id are never shown. |
| LP-10 | `rentalDays` counts days the same way as the fee rule in SRS §2.8 (return date minus pick-up date). The card shows "for 1 day", "for N days", or "for a week" when it is 7. |
| LP-11 | If the call fails (network error or `5xx`) or returns fewer than 3 reviews, the page still loads and the whole Reviews section is hidden, with no error message. The **Reviews** links in the header and footer are hidden too, so they never point at a missing section. |

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

## Open questions

1. Resolved: the reviews are static sample content (LP-21), so the company owner's quote can stay.
2. Only if the API option is built: are featured reviews picked automatically (LP-7) or by an admin? Admin picks need `Review.featured` and an admin screen that no mockup shows.
3. Resolved: one rating covers the vehicle and the service together, and counts toward both the vehicle's and the company's average. Reword the intro to: "After every completed rental, customers give one rating for the vehicle and the service together, so the next person knows what to expect."
4. Resolved: one cancellation rule for everyone (vehicle.md VEH-22, VEH-23). Reword How it works, step 03 to: "The rental company approves it, and you can cancel free until 24 hours before pick-up."
5. Resolved: a logged-in visitor sees the same landing page, with the account menu in place of **Log in** and **Sign up** (LP-24). No redirect for any role.
6. Resolved: search.md defines `GET /api/v1/places` and reads `type`, `location`, `from` and `to` from its URL.
7. Resolved: the earliest pick-up stays tomorrow (LP-3). Change the first review's quote to: "Found a scooter two streets from my hotel, booked it in a few minutes and picked it up the next morning."
8. Resolved: "See how it works" opens the static page `/for-companies`, Contact us is an email link, and Terms and Privacy are static text pages, which the sign-up form also links to (LP-25).
9. Resolved: the scene follows the clock (LP-19), the page follows the light or dark theme (LP-22), and the toggle sits in the header next to **Log in**, saved in `localStorage` (LP-23). A daytime demo still shows Day unless the URL pins `?time=`.
10. Resolved: the mockup was updated on 6 Nov 2026 to match LP-17 to LP-25: random scenery and camera, time from the clock, no Front ¾ or Side, the theme toggle and dark styles, the logged-in header (`?user=`), the reworded copy, and the four links. `/for-companies`, `/terms` and `/privacy` have no mockup yet; their links show a "comes later" toast.
