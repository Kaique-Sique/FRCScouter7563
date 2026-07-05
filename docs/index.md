# FRCScouter7563

[![License](https://img.shields.io/badge/License-MIT-blue)](https://github.com/Kaique-Sique/FRCScouter7563/blob/main/LICENSE) 
![Last Commit](https://img.shields.io/github/last-commit/Kaique-Sique/FRCScouter7563)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
[![FastAPI](https://img.shields.io/badge/framework-FastAPI-009688)](https://fastapi.tiangolo.com/)

Scouting and data API for the **FRC 2025 — Reefscape** season, built by team **Megazord 7563** (Jundiaí, SP, Brazil).

The project is a **FastAPI + PostgreSQL** backend with two major feature blocks:

1. **The Blue Alliance (TBA) API proxy** — teams, events, districts, matches, insights, and regional advancement, all consumed through the team's own [`BlueAlliancePy`](https://github.com/Kaique-Sique/BlueAlliancePy) library.
2. **In-house scouting** — endpoints to record and query on-field scouting data (autonomous, teleop, and pit scouting), persisted in the team's own PostgreSQL database.

> 🔎 For project overview, see [`docs/OVERVIEW.md`](/ReadTheDocs/OVERVIEW)
