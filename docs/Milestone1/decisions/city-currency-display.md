---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [search, vehicle, fees, dependencies]
repos: [rentxe]
---

# ADR — Pages show the city's currency; amounts stay in AUD

Context: The seed data has Melbourne and Ho Chi Minh City, and every price was shown in AUD, so a Saigon scooter read "A$12 / day" to Vietnamese customers.
Decision: Amounts are stored, worked out and returned in AUD everywhere. Each `CITY` place has a display `currency` (Melbourne `AUD`, Ho Chi Minh City `VND`), and pages show that city's currency: "199,000₫ / day" with a small "≈ A$12", rounded to 1,000₫. Spring fetches AUD rates once a day from ExchangeRate-API's open endpoint (no key), keeps them in memory, and serves them at `GET /api/v1/exchange-rates`; the page converts. The ₫ price slider is converted back to AUD before searching. A booking stores `displayCurrency` and `exchangeRate` when it is sent, so its ₫ amounts never move afterwards. Without a rate, pages fall back to A$.
Why: Vietnamese testers see prices they understand, while the fee, cancellation and late-return rules, and their tests, stay in one currency.
Rejected:
- AUD only: Saigon prices look wrong to local customers.
- Each city sets and charges in its own currency: every money rule and its tests would handle two currencies. Kept as a later option.
- Melbourne only: loses the Vietnam demo data.
Trade-off: a new outside dependency (SRS §7) that needs the "Rates By Exchange Rate API" link on pages showing ₫, and ₫ prices in search move slightly with the daily rate.
Links: SRS §2.3, §2.8, §7 · [api/search.md](../api/search.md) SR-28, endpoint 6, Q14 · [api/vehicle.md](../api/vehicle.md) VEH-41 · [api/README.md](../api/README.md) Money, Place, Booking, team decision 12
