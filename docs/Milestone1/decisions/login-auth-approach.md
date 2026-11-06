---
status: Open # options written down, nobody has chosen yet
date: 2026-11-06
decided-by: [] # the team, at stand-up
areas: [auth, security, architecture, supabase]
repos: [rentxe]
---

# ADR — How login works: Spring Security sessions or Supabase Auth (open)

Context: The team plans to use Supabase Postgres as the database. Supabase also offers an Auth service, so we have to choose who checks passwords and what the browser holds after log in. The diagram is in [architecture/auth-flows.html](../architecture/auth-flows.html), with a PNG in [auth-flows-a-vs-b.png](../architecture/auth-flows-a-vs-b.png) to share. Kept open on 2026-11-06 for the team to decide.

Option A, Spring Security sessions (recommended; the API docs are written for it):
- Spring checks the password against a BCrypt hash in our `users` table and keeps a server session. Supabase is only the database; its Auth feature stays off.
- The browser holds an `HttpOnly` `JSESSIONID` cookie that scripts can't read, plus a 14-day remember-me cookie when "Keep me logged in" is ticked.
- Log out and suspension take effect at once, because the session lives on the server.
- Sign-up creates the User and Company in one transaction, so the role can never go missing.
- Needs CSRF protection (Spring's token cookie and header). Reset emails are ours to build with Spring Mail.
- Tests run fully offline against H2, and all the security code is in our Spring app to show in SRS §3.2.

Option B, Supabase Auth on the page:
- The page signs users up and logs them in with Supabase's JavaScript library (supabase-js). Spring checks the Supabase JWT on each request against Supabase's public keys (JWKS).
- The browser holds a JWT and a refresh token in `localStorage`, which any script on the page can read. The library renews the JWT about every hour.
- A JWT keeps working for up to 1 hour after log out or suspension, unless Spring also checks `ACTIVE` on each request.
- Sign-up becomes two calls (Supabase, then Spring for the role and Company). If the second fails, the login has no role. The role must never come from `user_metadata`, which users can edit.
- No CSRF token needed, because the token goes in a header. Reset and confirmation emails are included, but the built-in sender is limited, so real use needs our own SMTP.
- Spring tests use fake JWTs; log in itself can't be tested without Supabase. Most of the security work happens inside Supabase, so check with the tutor that it still counts.

Not an option: Spring forwarding log in to the Supabase Auth API (it would combine the downsides of both). Convex instead of Supabase: its logic runs in TypeScript and it has no Java driver, which conflicts with Spring Boot.

Waiting on this choice: [api/login.md](../api/login.md) Q4 (reset emails), Q5 (CSRF), Q8 (throttling), Q9 (email confirmation) and the session length (LOGIN-17).
Decision: not made yet.
Links: [api/login.md](../api/login.md) Q16, LOGIN-12, LOGIN-15 to LOGIN-24 · [api/README.md](../api/README.md) Auth, team decision 10 · SRS §3.2, §4
