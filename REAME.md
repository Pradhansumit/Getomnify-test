# Omnify.com Test

A simple Booking API for a fictional fitness studio built with Django and Django REST Framework.

## Features

- View all upcoming fitness classes (`GET /api/classes/`)
- Book a spot in a class (`POST /api/book/`)
- View all bookings by email (`GET /api/bookings/?email=example@example.com`)
- Timezone-aware: Classes are created in IST; all slots adjust if timezone changes
- Handles overbooking, missing fields, and input validation
- Uses SQLite (in-memory or file-based) for storage
- Clean, modular, and well-documented code

## Setup Instructions

1. **Clone the repository**

   ```
   git clone https://github.com/Pradhansumit/Getomnify-test.git
   cd Getomnify-test
   ```

2. **Create a virtual environment and activate it**

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```
   pip install -r requirements.txt
   ```

4. **Apply migrations and seed data**

   ```
   python manage.py migrate
   python manage.py loaddata seed_data.json
   ```

5. **Run the server**
   ```
   python manage.py runserver
   ```

## Sample API Requests

- **Get all classes**

  ```
  curl -X GET http://localhost:8000/api/classes/
  ```

- **Book a class**

  ```
  curl -X POST http://localhost:8000/api/book/ \
    -H "Content-Type: application/json" \
    -d '{"class_id": 1, "client_name": "John Doe", "client_email": "john@example.com"}'
  ```

- **Get bookings by email**
  ```
  curl -X GET "http://localhost:8000/api/bookings/?email=john@example.com"
  ```

## Notes

- All class times are stored in IST (Asia/Kolkata). If you change the timezone in settings, class times and available slots will adjust accordingly.
- Handles errors such as overbooking, missing fields, and invalid input.
- Includes basic unit tests (see `api/tests.py`).
