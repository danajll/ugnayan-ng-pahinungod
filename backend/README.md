# UGNAYAN NG PAHINUNGOD — BACKEND

---

## Tech Stack
Django REST Framework 6.x + Python 3.x + Supabase (PostgreSQL)

---

## Prerequisites
- Python 3.13 or higher 
- A Supabase account (ask backend lead to provide access)

---

## Step 0: Navigate to backend dir
- cd backend

## Step 1: Create a Virtual Environment
- python -m venv venv

## Step 2: Activate the Virtual Env
- .\venv\Scripts\Activate.ps1
- Should now show (venv) before each prompt

## Step 3: Install dependencies
- pip install -r requirements.txt

## Step 4: Create .env
- Follow the provided .env.example file
- Ask backend devs if need help filling up

## Step 5: Run the Server
- python manage.py runserver

## Step 6: Verify if it works
- Run http://127.0.0.1:8000/api/health/ in your browser
- Should return {"status": "ok", "service": "backend"}

