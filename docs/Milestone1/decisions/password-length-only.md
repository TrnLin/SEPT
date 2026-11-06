---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [auth, security]
repos: [rentxe]
---

# ADR — Passwords: 8 to 72 characters, no other rules

Context: The mockup only says "At least 8 characters." The SRS needs an exact rule, and BCrypt, which stores the passwords, only reads the first 72 bytes.
Decision: A password has 8 to 72 characters and at most 72 bytes in UTF-8. It is not trimmed. There are no character-class rules and no common-password check (LOGIN-5).
Why: Matches the mockup hint and current NIST guidance, which favours length over forced symbols. The 72-byte cap stops two long passwords with the same first 72 bytes from both working.
Rejected:
- Upper case, lower case, digit and symbol rules: people answer with predictable patterns such as `Password1!`, and the hint and error messages would need rewriting.
- A common-password list: a cheap later upgrade for SRS §3.2, not needed for the MVP.
Links: SRS §2.1, §3.2 · [api/login.md](../api/login.md) LOGIN-5
