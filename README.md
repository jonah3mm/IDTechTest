# NetTrack — Developer Assessment

## Overview

NetTrack is a lightweight IT asset tracking tool used internally to manage client organizations and their devices. It lets technicians see at a glance which machines are active, inactive, or retired across all managed clients.

This repository is the starting point for our developer assessment. The app is functional but incomplete — it has bugs to find, features to build, and infrastructure to fix.

---

## The Role

We're an MSP hiring for a developer position that is roughly **60% application development** (bug fixes, new features, internal tooling) and **40% devops** (CI/CD, containerization, infrastructure). We build most of our internal tooling with Flask and Vue.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11, Flask, SQLAlchemy, SQLite |
| Frontend | Vue 3, Vite, Vue Router, Axios, Bootstrap 5 |
| Testing | pytest |
| Containers | Docker, Docker Compose |

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker (for Part 3)

### 1. Clone the repository

```bash
git clone <your-fork-url>
cd nettrack
```

### 2. Set up the backend

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python seed.py             # Populate the database with sample data
python run.py              # Start Flask on http://localhost:5000
```

### 3. Set up the frontend

In a separate terminal:

```bash
cd frontend
npm install
npm run dev                # Start Vite dev server on http://localhost:5173
```

Open **http://localhost:5173** in your browser. The Vite dev server proxies `/api` requests to Flask, so both services need to be running.

> **No environment variables are required for local development.** The app uses SQLite out of the box — a `nettrack.db` file will be created in the project root the first time you run `python run.py` or `python seed.py`.

---

## Your Tasks

This assessment is designed to take **2–4 hours**. We're not looking for perfection — we're looking for clear thinking, clean code, and good judgment about what to change and why.

**AI tools are fine.** What matters is the quality of what you turn in.

---

### Part 1: Bug Fixes

There are **6 bugs** in this codebase. Find and fix all of them.

The descriptions below tell you what's broken — locating the root cause is part of the task.

1. **Pagination doesn't advance.**
   The second page of assets always shows the same records as the first page, regardless of how many assets exist.

2. **Search is too strict.**
   Searching for `work` should return assets whose name contains "workstation." It doesn't — you have to type the full asset name exactly as stored.

3. **Status toggle misbehaves.**
   Clicking the toggle button on an *inactive* asset marks it as *retired* instead of restoring it to *active*.

4. **Deleting a client with assets fails.**
   Attempting to delete a client that still has assets assigned results in a server error instead of a graceful error response.

5. **The asset list crashes on missing dates.**
   When any asset has no "last seen" date on record, the asset list page throws a JavaScript error and fails to render entirely.

6. **Asset creation returns 500 on bad input.**
   Sending a `POST` request to create a new asset with required fields missing causes a 500 Internal Server Error rather than a validation error.

---

### Part 2: Feature Development

Implement all three features. Each has clear acceptance criteria — use your judgment on implementation details.

#### Feature 1: CSV Export

Add the ability to export the asset list as a CSV download.

**Acceptance criteria:**
- A new `GET /api/assets/export` endpoint returns a downloadable CSV file
- The export respects the same `search`, `type`, and `status` query parameters as the list endpoint
- The asset list page in the Vue frontend has an **Export CSV** button that triggers the download

#### Feature 2: Asset Audit Log

Track status changes over time so technicians can see when a device was toggled and by whom.

**Acceptance criteria:**
- A new database model records each status change: asset ID, previous status, new status, requester IP, and timestamp
- Status changes triggered by the toggle (and decommission) endpoints are logged automatically
- A new `GET /api/assets/<id>/audit` endpoint returns the change history for a given asset
- The asset detail page in the Vue frontend shows the audit history

#### Feature 3: Filter Controls

The backend already supports filtering by asset type and status via query parameters, but the frontend has no controls for these filters yet.

**Acceptance criteria:**
- The asset list page has dropdown controls for **Asset Type** and **Status**
- Changing a dropdown immediately re-fetches the list with the selected filter applied (no page reload)
- The selected filter values are reflected in the URL query string so pages can be bookmarked or shared

---

### Part 3: DevOps

#### Task 1: Fix the Docker Build

Build the image and run it:

```bash
docker build -t nettrack .
docker run -p 5000:5000 nettrack
```

The build succeeds, but something is wrong with the resulting container. Identify the problem, fix it, and also add a missing production dependency to `requirements.txt`.

#### Task 2: Fix the CI Pipeline

The `.github/workflows/ci.yml` workflow runs on every push and pull request. There's a problem with it — the pipeline always reports green, even when the test suite is failing. Fix the workflow so that tests are actually executed and CI fails when they break.

---

### Bonus (optional)

These are not required, but they're a good opportunity to show extra initiative:

- Write additional tests beyond the stubs in `tests/test_api.py`
- Add loading and error states to Vue components that are currently missing them
- Add server-side input validation and sanitization to API endpoints
- Improve the overall UX (search debouncing, confirmation modals, toast notifications, etc.)

---

## Submission

1. **Fork** this repository to your own GitHub account
2. Create a branch for your work (e.g., `yourname/assessment`)
3. Commit your changes with clear, descriptive commit messages
4. **Open a pull request** against `main` on this repository
5. In the PR description, briefly note:
   - Any tradeoffs or decisions you made
   - Anything you'd do differently with more time
   - Any bugs you found beyond the listed six (there shouldn't be any, but if you spot something, call it out)

---

## What We're Evaluating

| Area | What we look for |
|---|---|
| **Bug fixes** | Did you find the root cause, or just paper over the symptom? |
| **Feature implementation** | Does it work correctly, including edge cases? |
| **Code quality** | Is the code readable, idiomatic, and consistent with the existing style? |
| **Judgment** | Did you make sensible decisions when requirements left room for interpretation? |
| **Commits** | Are your commit messages informative? Is the history easy to follow? |
| **DevOps** | Do you understand what's actually wrong with the Docker and CI setup? |

We are **not** evaluating how fast you worked or whether you used AI. We're evaluating the quality of what you submit.
