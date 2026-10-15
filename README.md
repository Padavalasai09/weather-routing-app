# Weather Routing App

A full-stack assessment app built with Django + Django REST Framework on the backend and React + Material UI on the frontend. The app helps travelers compare route options using weather comfort, rain exposure, and wind risk.

## Tech stack

- Backend: Django 5 + DRF
- Frontend: React + Vite + Material UI
- Database: SQLite (local development)

## Local setup

### 1. Backend

```bash
cd backend
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Then open the app at http://localhost:5173.

## API

- GET http://localhost:8000/api/health/
- POST http://localhost:8000/api/routes/plan/

Example payload:

```json
{
  "origin": "Seattle",
  "destination": "Austin",
  "departure_date": "2026-10-15",
  "preferred_temperature_c": 22
}
```

## Project goals

- Model a realistic weather-aware route decision system
- Deliver a clean, responsive UI built with Material UI
- Expose a REST API with algorithmic scoring and route ranking
- Show how backend logic and user experience can work together end-to-end
