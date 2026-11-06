---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [search, ui, dates]
repos: [rentxe]
---

# ADR — Search defaults: dates count from the place, the place is the last one searched

Context: The server checks "pick-up after today" in the searched place's time zone, but the landing page picks default dates from the visitor's clock. Near midnight they disagree: at 23:30 on 6 Nov in Ho Chi Minh City it is already 7 Nov in Melbourne. And with no place in the URL, the search page always started at Melbourne CBD.
Decision: Once a place is known, the search page counts default dates (tomorrow, for 3 days) in the place's time zone, and moves a pick-up that is already "today" there to tomorrow, keeping the rental length, with no error. The page saves the last searched place in `localStorage` (`rentxe-last-place`) and uses it when the URL has no place; otherwise Melbourne CBD.
Why: The server's `400` should never come from dates the visitor didn't pick. Remembering the place helps returning visitors in Vietnam, likely most of our testers. Both are page-only, with no API change.
Rejected:
- Accepting the mismatch and showing the `400`: an error from dates the visitor never chose.
- Always defaulting to Melbourne CBD: Saigon users would switch city every visit.
Trade-off: the remembered place is per browser, not per account.
Links: SRS §2.3 · [api/search.md](../api/search.md) SR-4, SR-27, Q11 · [api/landing.md](../api/landing.md) LP-2
