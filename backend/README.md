# UGNAYAN NG PAHINUNGOD — BACKEND

---

## Tech Stack
Django REST Framework 6.x + Python 3.x + Supabase (PostgreSQL)

---

## Prerequisites
- Python 3.13 or higher 
- A Supabase account (ask backend lead to provide access)

---

### Full Setup
pip install -r requirements.txt
cp .env.example .env       
python manage.py migrate
python manage.py seed_lookups
python manage.py runserver


### Running the Server
'''bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1


### Environment Variables (.env)
| Variable               | Description                                          |
|------------------------|------------------------------------------------------|
| `DJANGO_SECRET_KEY`    | Django secret key                                    |
| `DJANGO_DEBUG`         | Set to `True` in development, `False` in production  |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated allowed hosts                        |
| `DATABASE_URL`         | Supabase Postgres connection string                  |
| `SUPABASE_URL`         | Supabase project URL                                 |
| `SUPABASE_KEY`         | Supabase anon public key                             |
| `GOOGLE_CLIENT_ID`     | Google OAuth 2.0 Client ID                           |
| `GOOGLE_CLIENT_SECRET` | Google OAuth 2.0 Client Secret                       |

Note: Make sure to ask backend devs to fill this up
---

# API Guide
**Base URL:** `http://127.0.0.1:8000/api`

## Authentication

The API uses **token authentication**. Get a token by signing in with Google (volunteers) or logging in with username/password (admin fallback).

### Google OAuth Sign-In 

1. Frontend gets an **ID token** from Google Sign-In JS library
2. POST the ID token to `/api/auth/google/`
3. Backend verifies it, checks the `@up.edu.ph` domain, creates (or fetches) the User + Volunteer, and returns a Django auth token

**Only `@up.edu.ph` Google accounts are allowed.**

**Request:**
```
http
POST /api/auth/google/
Content-Type: application/json

{
  "id_token": "token-here"
}
```

**Sample 201 Response**
```
json
{
  "token": "279816e84b8b2c555de362a28b550faeee798e39",
  "user_id": 2,
  "email": "kojose2@up.edu.ph",
  "volunteer_id": 2,
  "is_profile_complete": false,
  "created": true
}
```


**Note:** `is_profile_complete` tells the frontend whether to route the user to onboarding (fill-up form) or the dashboard. If true, that means the user has completed the forms and is officially part of the organization. If false, that means the user still needs to complete the profile creation forms.

### Username/Password Login (Admin Fallback)

**Request:**
```
http
POST /api/login/
Content-Type: application/json

{
  "username": "test-user",
  "password": "TestPass123!"
}
```

**Response:**
```
json
{
  "token": "abc123...",
  "user_id": 1,
  "username": "test_user",
  "is_staff": false,
  "is_superuser": false
}
```

### Using the Token

For any endpoint, add this header:

```
http
Authorization: Token 279816e84b8b2c555de362a28b550faeee798e39
```

**Common mistake:** Do NOT include the `Authorization` header on public endpoints (register, login, google). DRF rejects the request before the view runs if a stale token is present.

---

## Endpoint Reference

###  Public Endpoints

| Method| Endpoint             | Description                                            |
|-------|-----------------------|--------------------------------------------------------|
| GET   | `/api/health/`        | Health check — `{"status": "ok"}`                      |
| POST  | `/api/register/`      | Legacy admin-fallback registration (username/password) |
| POST  | `/api/login/`         | Log in with username/password                          |
| POST  | `/api/auth/google/`   | Sign in with Google ID token                           |
| GET   | `/api/events/`        | List all events                                        |
| POST  | `/api/events/`        | Create an event (admin only)                           |
| GET   | `/api/events/<id>/`   | Retrieve one event                                     |
| PUT   | `/api/events/<id>/`   | Full update (admin only)                               |
| PATCH | `/api/events/<id>/`   | Partial update (admin only)                            |
| DELETE| `/api/events/<id>/`   | Delete (admin only)                                    |
| GET   | `/api/programs/`      | List all volunteer programs                            |
| GET   | `/api/subjects/`      | List all affirmative-action subjects                   |

### 🔒 Authenticated Endpoints
Require header tokens: `Authorization: Token <your-token>`

| Method| Endpoint                         | Description                                       |
|-------|----------------------------------|---------------------------------------------------|
| PATCH | `/api/volunteers/me/onboarding/` | Save the full onboarding form                     |
| GET   | `/api/volunteers/me/profile/`    | Read optional profile info                        |
| PATCH | `/api/volunteers/me/profile/`    | Update profile information                        |
| POST  | `/api/events/<id>/join/`         | Join an event                                     |
| GET   | `/api/me/participations/`        | List your own event registrations                 |
| PATCH | `/api/participations/<id>/`      | Cancel your registration                          |
| DELETE| `/api/participations/<id>/`      | Remove your registration                          |
| GET   | `/api/volunteers/`               | List all volunteers (ADMIN ONLY)                  |
| GET   | `/api/volunteers/<id>/`          | Retrieve one volunteer (ADMIN ONLY)               |
| PATCH | `/api/volunteers/<id>/`          | Partial update (ADMIN ONLY)                       |

