# Decisions

Every decision and every revision made during the milestone, one file per decision. Canvas: "Document all decisions and revisions made during the milestone in the project repository's documentation folder."

**Reading:** scan the index below and open only the files you need. To search by topic, grep the front matter, for example `grep -l "areas:.*booking" *.md`.

**Adding a decision:**
1. Copy the template below into `<slug>.md`. The slug is a few lowercase words joined by hyphens, for example `one-cancellation-rule`.
2. Add a row to the index.
3. To replace a decision, write a new file. Then set the old file's status to `Superseded by ADR-<new-slug>` and update its row. Never delete an old file.

**Status:** `Open` means the options are written down but nobody has chosen yet. `Proposed` means not yet agreed by the team, so confirm it at stand-up. The other values are `Accepted`, `Superseded by ADR-<slug>` and `Deprecated`.

## Index

| Decision | Status | Areas | Summary |
|---|---|---|---|
| [login-auth-approach](login-auth-approach.md) | Proposed | auth, security, architecture | Spring Security sessions with an HttpOnly cookie; Supabase is only the database, its Auth is not used |
| [api-schema-per-page](api-schema-per-page.md) | Proposed | api, srs | One API file per mockup page in `api/`, with numbered rules for the SRS |
| [static-landing-reviews](static-landing-reviews.md) | Proposed | landing, reviews, api | Landing reviews are fixed sample text, so there is no featured-reviews endpoint |
| [one-rating-per-review](one-rating-per-review.md) | Proposed | reviews, data-model | One rating covers the vehicle and the service, and counts toward both averages |
| [one-cancellation-rule](one-cancellation-rule.md) | Proposed | booking, fees | Free until 24 h before pick-up, then 50% of the total, the same for every company |
| [earliest-pickup-tomorrow](earliest-pickup-tomorrow.md) | Proposed | booking, search, landing | No same-day rentals, because the company must approve first |
| [logged-in-landing-same-page](logged-in-landing-same-page.md) | Proposed | landing, auth, ui | Logged-in visitors stay on the landing page and get the account menu, with no redirect |
| [landing-hero-random-scene](landing-hero-random-scene.md) | Proposed | landing, 3d, ui | Random scenery and camera on each load, and time of day from the visitor's clock |
| [light-dark-theme](light-dark-theme.md) | Proposed | theme, ui, design-tokens | System, Light and Dark toggle saved in `localStorage`; the 3D scene is not themed |
| [static-company-legal-pages](static-company-legal-pages.md) | Proposed | landing, ui, static-pages | Static `/for-companies`, `/terms` and `/privacy` pages; Contact us is an email link |
| [company-signup-contact-person](company-signup-contact-person.md) | Proposed | auth, signup, company | Company sign-up also asks for the registering person's name and a phone number, so an admin can call before verifying |
| [unverified-company-setup-hidden](unverified-company-setup-hidden.md) | Proposed | company, admin, search | Unverified companies set up while hidden; only verified companies with an active account are public; rejecting means suspending |
| [customer-landing-after-login](customer-landing-after-login.md) | Proposed | auth, ui, booking | After sign-up customers go to Search; after log in, to My bookings only with an active booking |
| [return-to-page-after-login](return-to-page-after-login.md) | Proposed | auth, ui, security | After log in or sign-up, customers return to the page in `?next=`, only if it is on our own site |
| [logged-in-user-skips-login-page](logged-in-user-skips-login-page.md) | Proposed | auth, ui | A logged-in user who opens the login page is sent where a fresh log in would send them |
| [one-seeded-admin](one-seeded-admin.md) | Proposed | auth, admin, security | One admin seeded at start-up from settings; promoting other accounts to admin comes later |
| [password-length-only](password-length-only.md) | Proposed | auth, security | Passwords are 8 to 72 characters with no other rules |
| [one-role-per-account](one-role-per-account.md) | Proposed | auth, data-model, security | Each account is a customer, a company or an admin, never more than one |
| [password-reset-views-and-email](password-reset-views-and-email.md) | Proposed | auth, email, ui | Forgot and reset views on the login page; Spring Mail with Mailpit in dev and Brevo when deployed |
| [no-email-confirmation-mvp](no-email-confirmation-mvp.md) | Proposed | auth, email, signup | New accounts work straight away; no email confirmation in the MVP |
| [csrf-token-cookie](csrf-token-cookie.md) | Proposed | auth, security, api | Spring's CSRF protection stays on, with a readable token cookie and a header sent by a shared fetch wrapper |
| [login-throttle-only](login-throttle-only.md) | Proposed | auth, security | One throttle: 5 failed log ins per email and IP in 15 minutes blocks for 15 minutes; no reset email limit |
| [session-defaults](session-defaults.md) | Proposed | auth, security, config | 30 minutes idle or 14 days with remember-me; sessions in memory; signed remember-me cookie |
| [form-error-banner](form-error-banner.md) | Proposed | ui, auth, accessibility | Field errors under the field; other errors in a banner at the top of the form, never a toast |
| [static-help-page](static-help-page.md) | Proposed | ui, static-pages, auth | Help opens a static `/help` FAQ about accounts and renting, for every visitor |
| [unique-company-names](unique-company-names.md) | Proposed | company, signup, data-model | Company names are unique, ignoring case and extra spaces, so look-alikes can't borrow reviews |
| [one-listing-one-vehicle](one-listing-one-vehicle.md) | Proposed | search, vehicle, booking, data-model | One listing is one physical vehicle; no `units`, and the "Only N left" label is dropped |
| [requests-hold-dates-and-expire](requests-hold-dates-and-expire.md) | Proposed | booking, search, vehicle, data-model | Requests block their dates; unanswered after 24 h (or by the pick-up day) they become `EXPIRED` |
| [return-day-stays-blocked](return-day-stays-blocked.md) | Proposed | booking, search, vehicle | A booking blocks its return day too; the next pick-up is the day after at the earliest |
| [booked-vehicles-shown-flagged](booked-vehicles-shown-flagged.md) | Proposed | search, ui | Booked vehicles stay in search results, flagged; the headline says how many are free for the dates |
| [rental-length-and-horizon](rental-length-and-horizon.md) | Proposed | booking, search, vehicle | A booking is at most 30 days and starts at most 12 months ahead |
| [extend-rental-by-30-days](extend-rental-by-30-days.md) | Proposed | booking, data-model | From the last week of a rental, the customer can ask for up to 30 more days; the company approves |

## Template

```markdown
---
status: Proposed # Open | Proposed | Accepted | Superseded by ADR-<slug> | Deprecated
date: YYYY-MM-DD
decided-by: [Name]
areas: [tag] # greppable tags
repos: [rentxe]
---

# ADR — Title

Context: <the situation, 1-2 lines>
Decision: <what we chose, 1-2 lines>
Why: <the deciding reasons, 2-3 lines>
Rejected: <alternatives and the one-line reason each lost>
Links: <ticket, MR, related ADR, SRS section, rule IDs>
```
