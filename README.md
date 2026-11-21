# Ugnayan ng Pahinungod — Frontend

Vue 3 + Vite frontend for the volunteer management app. Proxies `/api` to the Django backend at `http://127.0.0.1:8000`.

## Tech Stack
- Vue 3 (`<script setup>`)
- Vite 5
- Vue Router 4
- Axios

## Prerequisites
- Node.js 18+ and npm

## Setup
```bash
npm install
cp .env.example .env   # set VITE_GOOGLE_CLIENT_ID
```

## Run
```bash
npm run dev            # Vite dev server on http://localhost:5173
npm run build          # production build
npm run preview        # preview production build
```

## Environment Variables (root `.env`)
| Variable | Description |
|---|---|
| `VITE_GOOGLE_CLIENT_ID` | Google OAuth 2.0 Client ID (used by Google Sign-In) |

## Work Flow
1. Start the Django backend first (`backend/`, port 8000) — see `backend/README.md`.
2. Start this dev server on port 5173.
3. Vite proxies `/api` requests to the backend; no CORS issues in dev.
4. Sign in with a `@up.edu.ph` Google account. New users are routed to onboarding; returning users go to the dashboard.
5. Volunteers browse events/programs, join events, and manage their profile. Admins manage volunteers/events.

## Project Structure
```
src/
  api/       # Axios API clients (auth, events, volunteers, ...)
  router/    # Vue Router routes
  views/     # Pages: sign/, user/, admin/
  styles/    # Shared CSS
  main.js
  App.vue
```

## Auth Quirks
- Token auth: header `Authorization: Token <token>`, stored client-side after login.
- Do NOT send `Authorization` on public endpoints (`/api/register/`, `/api/login/`, `/api/auth/google/`).
- Only `@up.edu.ph` Google accounts are allowed.
