---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [theme, ui, design-tokens, landing]
repos: [rentxe]
---

# ADR — Light and dark theme on every page, saved in the browser

Context: We wanted the hero scene to follow the clock and the site to support light and dark mode as well. No page had a dark theme.
Decision: Every page has a light and a dark theme. It starts from the system setting (`prefers-color-scheme`). A toggle that cycles System, Light and Dark sits in the header next to **Log in**, or next to the account menu when logged in. The choice is saved in `localStorage` under `rentxe-theme`, and a small script in `<head>` applies it before the page draws, so it never flashes the wrong theme. The colours are `--theme-*` tokens in `assets/mockups/shared/tokens.css`, still orange, black and white. The 3D hero scene and the search box over it are not themed (LP-22).
Why: It improves usability at no backend cost. Keeping the theme and the scene's time of day separate means neither setting overrides the other.
Rejected:
- Saving the theme on the user's account: it needs a `User.theme` field and a profile endpoint. Its only gain is following the user to another device, which the MVP doesn't need.
- The theme driving the scene's time of day: see [landing-hero-random-scene](landing-hero-random-scene.md).
Links: SRS §3.3 (suggested: every page readable in both themes, text contrast at least 4.5:1), §5 · [api/README.md](../api/README.md) Theme · [api/landing.md](../api/landing.md) LP-22, LP-23 · To do: dark styles and the toggle on the login, search and vehicle mockups
