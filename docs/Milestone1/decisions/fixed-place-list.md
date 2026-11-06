---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [search, data-model]
repos: [rentxe]
---

# ADR — "Where" suggests places from a fixed list

Context: The search page's "Where" field suggests places as the customer types, and the picked place sets the distances, the city searched and the map centre. The list could come from our own table or from an outside geocoder that knows every address.
Decision: A fixed `Place` table that the team seeds at start-up: the cities, suburbs or districts, and airports where companies list vehicles, each with hidden other names such as "Saigon" and "HCMC". Customers can only pick from it. Open search through a geocoder (Mapbox Search, Google Places) is noted as a later option: the page would send `lat` and `lng` instead of `placeId`, so the search API needs no redesign.
Why: Free, offline and quick; tests need no network or mocks; every suggestion has vehicles nearby. The mockup only ever suggests a few fixed places.
Rejected:
- Open search through a geocoder in the MVP: an account, an API key, usage limits, mocks in tests, and places with no vehicles. Mapbox's free geocoding results also can't be stored.
Trade-off: a street address or landmark can't be typed, and someone adds rows by hand for each new city.
Links: SRS §2.3, §7 · [api/search.md](../api/search.md) Q7, places endpoint notes · [api/README.md](../api/README.md) Place
