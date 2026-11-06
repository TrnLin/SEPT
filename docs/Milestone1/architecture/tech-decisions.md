# Technology decisions

The rubric asks for the reason behind every choice. Fill in "Why" and "Alternatives considered" as a team.

| Component | Technology | Why we chose it | Alternatives considered |
|---|---|---|---|
| Language | Java 21 (same version for everyone) | Because the Assignment said so | Typescript everyday|
| Web framework | Spring Boot | We have no other choice else we get annihilate| |
| Build | Maven | | |
| Frontend | HTML/CSS/JavaScript or React (pick one) | | |
| Database | H2 (dev/test) or MySQL (pick one) | | |
| Login / auth | Spring Security sessions (option A) | Password checks and sessions stay in our Spring app, testable offline; logout and suspension work at once. See [login-auth-approach](../decisions/login-auth-approach.md) and [auth-flows.html](auth-flows.html) | |
| Email | Spring Mail over SMTP: Mailpit (dev), fake sender (tests), Brevo free SMTP (deployed) | Settings only, so the provider can change without code; Brevo needs no domain | Resend (needs a domain we own; switch later if we buy one), Gmail app password, logging the link only |
| Map | Leaflet with OpenStreetMap-based tiles (a light and a dark set, following the theme) | Free, open source, no account or key; markers and circles cover the search map. See [leaflet-openstreetmap-map](../decisions/leaflet-openstreetmap-map.md) | Mapbox GL JS (more polished, needs an account and a token; free up to 50,000 map loads a month) |
| Place search | A fixed, seeded `Place` table | No outside service; every suggestion has vehicles nearby. See [fixed-place-list](../decisions/fixed-place-list.md) | Mapbox Search or Google Places for open address search (later option) |
| Exchange rates | ExchangeRate-API open endpoint, fetched once a day by Spring | No key; covers VND; shows A$ or ₫ by city while amounts stay AUD. Needs the "Rates By Exchange Rate API" link. See [city-currency-display](../decisions/city-currency-display.md) | Frankfurter (ECB rates, likely no VND), Open Exchange Rates or Fixer (need a key) |
| Unit tests | JUnit 5 | | |
| CI/CD | GitHub Actions | | |
| Containers | Docker | | |

Save the architecture diagram in this folder (for example `architecture-diagram.png`) and embed it in SRS section 4.
