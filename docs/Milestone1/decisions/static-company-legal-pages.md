---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [landing, ui, static-pages]
repos: [rentxe]
---

# ADR — Static pages for companies, Terms and Privacy

Context: Four landing links went nowhere (`href="#"`): "See how it works" in the company section, and Contact us, Terms and Privacy in the footer. The sign-up form asks users to agree to Terms and Privacy, so those links must lead somewhere real.
Decision: "See how it works" opens `/for-companies`, a static page that explains the company side in six steps and ends with **Register your company**. `/terms` and `/privacy` are plain text pages with placeholder text. Contact us is a `mailto:` link. None of them needs an API (LP-25). Until they are mocked up, the mockup shows a "comes later" message.
Why: No dead links, and the sign-up agreement points at real pages. Static pages cost no backend work.
Rejected:
- Removing the "See how it works" button: it is simpler, but companies get no explanation of how RentXe works for them.
- A contact form or page: more to build and test, for no gain over an email link.
Links: SRS §5 (three more screens, each needs a simple wireframe) · [api/landing.md](../api/landing.md) LP-25, Q8
