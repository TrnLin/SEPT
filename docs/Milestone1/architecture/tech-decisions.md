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
| Unit tests | JUnit 5 | | |
| CI/CD | GitHub Actions | | |
| Containers | Docker | | |

Save the architecture diagram in this folder (for example `architecture-diagram.png`) and embed it in SRS section 4.
