---
status: Proposed # to confirm at stand-up
date: 2026-11-06
decided-by: [Linh Tran]
areas: [booking, search, vehicle]
repos: [rentxe]
---

# ADR — The return day stays blocked

Context: Every pick-up and return is at 10:00, so a vehicle could in theory be returned and picked up again on the same day. The vehicle calendar mockup shows the return day as booked, but the team had not decided it.
Decision: A booking blocks every day from its `startDate` to its `endDate`, both included. A vehicle returned on Mon 14 Dec can next be picked up on Tue 15 Dec. A range clashes with a booking when `booking.startDate <= endDate` and `booking.endDate >= startDate`.
Why: The day gives the company time to clean and check the vehicle, and a late return can't make the next customer wait at the desk. It matches the calendar mockup and keeps one simple overlap check, with no "free from 10:00" state.
Rejected:
- The return day is free for a new pick-up: both customers would be at the desk at 10:00, and a late return becomes the next customer's problem.
Trade-off: the vehicle sits idle for one day between back-to-back rentals.
Links: SRS §2.4, §2.8 · [api/vehicle.md](../api/vehicle.md) VEH-6, VEH-7, Q3 · [api/search.md](../api/search.md) SR-7, Q2 · [api/README.md](../api/README.md) team decision 3
