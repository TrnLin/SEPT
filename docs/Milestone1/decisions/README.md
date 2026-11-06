# Decisions

Every decision and every revision made during the milestone, one file per decision. Canvas: "Document all decisions and revisions made during the milestone in the project repository's documentation folder."

**Reading:** scan the index below and open only the files you need. To search by topic, grep the front matter, for example `grep -l "areas:.*booking" *.md`.

**Adding a decision:**
1. Copy the template below into `<slug>.md`. The slug is a few lowercase words joined by hyphens, for example `one-cancellation-rule`.
2. Add a row to the index.
3. To replace a decision, write a new file. Then set the old file's status to `Superseded by ADR-<new-slug>` and update its row. Never delete an old file.

**Status:** `Proposed` means not yet agreed by the team, so confirm it at stand-up. The other values are `Accepted`, `Superseded by ADR-<slug>` and `Deprecated`.

## Index

| Decision | Status | Areas | Summary |
|---|---|---|---|
| [api-schema-per-page](api-schema-per-page.md) | Proposed | api, srs | One API file per mockup page in `api/`, with numbered rules for the SRS |
| [static-landing-reviews](static-landing-reviews.md) | Proposed | landing, reviews, api | Landing reviews are fixed sample text, so there is no featured-reviews endpoint |
| [one-rating-per-review](one-rating-per-review.md) | Proposed | reviews, data-model | One rating covers the vehicle and the service, and counts toward both averages |
| [one-cancellation-rule](one-cancellation-rule.md) | Proposed | booking, fees | Free until 24 h before pick-up, then 50% of the total, the same for every company |
| [earliest-pickup-tomorrow](earliest-pickup-tomorrow.md) | Proposed | booking, search, landing | No same-day rentals, because the company must approve first |
| [logged-in-landing-same-page](logged-in-landing-same-page.md) | Proposed | landing, auth, ui | Logged-in visitors stay on the landing page and get the account menu, with no redirect |
| [landing-hero-random-scene](landing-hero-random-scene.md) | Proposed | landing, 3d, ui | Random scenery and camera on each load, and time of day from the visitor's clock |
| [light-dark-theme](light-dark-theme.md) | Proposed | theme, ui, design-tokens | System, Light and Dark toggle saved in `localStorage`; the 3D scene is not themed |
| [static-company-legal-pages](static-company-legal-pages.md) | Proposed | landing, ui, static-pages | Static `/for-companies`, `/terms` and `/privacy` pages; Contact us is an email link |

## Template

```markdown
---
status: Proposed # Proposed | Accepted | Superseded by ADR-<slug> | Deprecated
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
