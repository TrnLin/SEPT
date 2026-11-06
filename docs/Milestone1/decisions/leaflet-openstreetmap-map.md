---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [search, ui, dependencies]
repos: [rentxe]
---

# ADR — The search map uses Leaflet with OpenStreetMap-based tiles

Context: The search mockup draws a stylised SVG map. The real page needs a map library and map tiles for the price pins, the 2 / 5 / 10 km rings and the "you" dot, in both themes.
Decision: Leaflet, with OpenStreetMap-based tiles: a light tile set, and a dark one (for example CARTO's) when the theme is dark. The map shows "© OpenStreetMap contributors" and the tile provider's credit. Leaflet, OpenStreetMap and the tile provider are listed in SRS §7.
Why: Free and open source, with no account, key or card for anyone on the team. Markers and circles cover everything the mockup's map does.
Rejected:
- Mapbox GL JS: smoother zoom and built-in dark styles, but it needs an account and a public token restricted to our domain, and may ask for a card. Worth it only for a more polished look.
Trade-off: free tile servers are meant for light use. That's fine for the course demo; a real launch would need a paid or self-hosted tile provider. Check the chosen provider's terms before the demo.
Links: SRS §2.3, §7 · [api/search.md](../api/search.md) SR-21, Q9 · [architecture/tech-decisions.md](../architecture/tech-decisions.md) Map
