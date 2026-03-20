# Carbnb: Multi-Vendor Car Rental Platform

A modern, multi-vendor car rental platform built with Django 5.2 and Bootstrap.

## Features
- Multi-vendor system: Vendor registration, car listings, dashboard
- Customer features: Browse/search/filter cars, booking, booking history
- Admin panel: Approve vendors/cars, manage fees, monitor rentals
- Elegant, mobile-friendly UI
- Image gallery with drag-and-drop, multi-upload, and reordering

## Tech Stack
- Django 5.2
- Bootstrap 5
- Pillow (image processing)
- Chart.js (for analytics, optional)

## Setup
1. **Clone the repo:**
   ```bash
   git clone <your-repo-url>
   cd car_rental
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run migrations:**
   ```bash
   python manage.py migrate
   ```
4. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```
5. **Run the server:**
   ```bash
   python manage.py runserver
   ```
6. **Access the app:**
   - Home: [http://localhost:8000/](http://localhost:8000/)
   - Admin: [http://localhost:8000/admin/](http://localhost:8000/admin/)

## Media & Static Files
- Uploaded images are stored in `/media/`.
- For development, media files are served automatically.

## Customization
- To use PostgreSQL, update `DATABASES` in `car_rental/settings.py`.

## License
MIT 
