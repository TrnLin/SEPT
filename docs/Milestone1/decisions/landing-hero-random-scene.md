---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [landing, 3d, ui]
repos: [rentxe]
---

# ADR — Random hero scene, time of day from the clock

Context: The 3D landing hero had fixed scenery, time and camera. The prototype also wrote them into the URL, so a reload repeated the same look. There were five cameras.
Decision: Each load picks Mountains or City at random (LP-17) and the Scenic, Chase or Top camera at random (LP-18). Front ¾ and Side are removed. The time of day comes from the visitor's clock: Day 07:00 to 16:59, Sunset 05:00 to 06:59 and 17:00 to 19:59, Night 20:00 to 04:59 (LP-19). `?scenery=`, `?camera=` and `?time=` pin one look for screenshots and demos, and the page never writes them back (LP-20). Phones show the static photo, so none of this applies there.
Why: Each visit looks a bit different, and the sky matches the visitor's day. Three cameras keep the shots that read best.
Rejected:
- Time of day from the light or dark theme: the theme is now a separate setting ([light-dark-theme](light-dark-theme.md)), and the clock shows all three skies over a day. The cost: a daytime demo always shows Day unless you add `?time=sunset`.
- Keeping Front ¾ and Side: not wanted.
Links: SRS §5 · [api/landing.md](../api/landing.md) LP-17 to LP-20 · `assets/mockups/landing-3d/index.html`
