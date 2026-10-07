# UGNAYAN NG PAHINUNGOD — BACKEND

---

## Tech Stack
Django REST Framework 6.x + Python 3.x + Supabase (PostgreSQL)

---

## Prerequisites
- Python 3.13 or higher 
- A Supabase account (ask backend lead to provide access)

---

## Run
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env                 # Fill in real values
python manage.py migrate
python manage.py runserver

---

## Run
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env                 # Fill in real values
python manage.py migrate
python manage.py runserver

---

## Guide to the APIs
1. BASE URL
http://127.0.0.1:8000/api

2. Authentication
Most endpoints are public. Endpoints marked with a lock (🔒) require a token.

3. Summary of Endpoints

## Public Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health/` | Used for testing, confirms if the backend is running |
| POST | `/api/register/` | Create a new volunteer account (returns an auth token) |
| POST | `/api/login/` | Log in with existing credentials (returns an auth token) |
| GET | `/api/events/` | List all events |
| POST | `/api/events/` | Create a new event |
| GET | `/api/events/<id>/` | Retrieve a single event |
| PUT | `/api/events/<id>/` | Full update of an event |
| PATCH | `/api/events/<id>/` | Partial update of an event |
| DELETE | `/api/events/<id>/` | Delete an event |
| GET | `/api/volunteers/` | List all volunteers |
| GET | `/api/volunteers/<id>/` | Retrieve a single volunteer |

## Authenticated Endpoints 🔒

Require header: `Authorization: Token <your-token>`

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/events/<id>/join/` | Join an event (creates a participation) |
| GET | `/api/me/participations/` | List your own event registrations |
| PATCH | `/api/participations/<id>/` | Cancel your registration (sets `status` to `cancelled`) |
| DELETE | `/api/participations/<id>/` | Remove your registration entirely |
| GET | `/api/volunteers/me/profile/` | Read your optional profile details (contact, address, background, emergency) |
| PATCH | `/api/volunteers/me/profile/` | Update any subset of your profile sections |