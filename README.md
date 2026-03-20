# Carbnb: Multi-Vendor Car Rental Platform

A multi-vendor car rental platform with a Django REST API backend and a Vite + React frontend.

## Features
- Multi-vendor onboarding and car listings
- Customer booking, return confirmation, reviews
- Vendor withdrawal requests
- Admin approval flows and analytics summary
- JWT-based authentication

## Tech Stack
- Django 5.2 + Django REST Framework
- SimpleJWT (JWT auth)
- MySQL (default in settings.py)
- Vite + React + React Router
- Axios

## Backend Setup
1. **Clone & install**
   ```bash
   git clone <your-repo-url>
   cd Car-rental-ycj-new
   pip install -r requirements.txt
   ```
2. **Configure database**
   - Edit `car_rental/settings.py` if you want to use a different database.
3. **Run migrations**
   ```bash
   python manage.py migrate
   ```
4. **Create admin user**
   ```bash
   python manage.py createsuperuser
   ```
5. **Start backend**
   ```bash
   python manage.py runserver
   ```

Backend base URL: `http://localhost:8000/`

## Frontend Setup
1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```
2. **Start frontend**
   ```bash
   npm run dev
   ```

Frontend URL: `http://localhost:5173/`

The frontend calls the backend API at `http://localhost:8000/api`.

## Authentication (JWT)
- **Login**: `POST /api/token/` with `{ "username": "...", "password": "..." }`
- **Refresh**: `POST /api/token/refresh/` with `{ "refresh": "..." }`

Store the `access` token in local storage and send as:
`Authorization: Bearer <token>`

## API Endpoints (Summary)
- **Cars**: `GET /api/cars/`, `GET /api/cars/<id>/`
- **Bookings**: `GET /api/bookings/`, `POST /api/bookings/create/`, `POST /api/bookings/<id>/return/`
- **Reviews**: `GET /api/reviews/`, `POST /api/reviews/create/`, `POST /api/reviews/<id>/reply/`
- **Withdrawals**: `POST /api/withdrawals/`
- **Admin**: `POST /api/admin/bookings/<id>/approval/`, `POST /api/admin/cars/<id>/approval/`, `POST /api/admin/withdrawals/<id>/`
- **Analytics**: `GET /api/analytics/summary/`

## Media & Static Files
- Uploaded images are stored in `/media/` and served automatically in development.

## License
MIT