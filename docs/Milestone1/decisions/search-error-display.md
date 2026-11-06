---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [search, ui, accessibility]
repos: [rentxe]
---

# ADR — Where errors show on the search page

Context: The search mockup only has a toast, but we decided for login that errors never go in a toast, because toasts vanish and screen readers miss them ([form-error-banner](form-error-banner.md)). Search isn't a submitted form, so the login banner doesn't fit it exactly.
Decision: When search or facets fail, the results area shows "Couldn't load results." with a Try again button (`role="alert"`), the old results are cleared and the filters stay usable. Field errors show under their field: "No place matches" under Where, a date `400` under that date with the server's message. Side calls fail quietly: no rate shows A$, no booking count hides the number, a failed compare refill clears the tray. The toast is only for notices.
Why: The results area is where people look when results don't come, and the message sits next to its fix. It follows the same no-errors-in-toasts rule as login.
Rejected:
- A banner at the top, as on login: search has no single submit, and the banner would sit far from the results.
- Toasts: they vanish and are poor for accessibility.
Trade-off: a results-area error state to add to the mockup.
Links: SRS §2.3, §3.3 · [api/search.md](../api/search.md) SR-29, Q16 · [api/login.md](../api/login.md) LOGIN-32
