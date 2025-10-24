# Django Barber Shop Management System

A personal study project for Django - a complete barber shop appointment management application.

## Project Structure

```
barber_shop/
├── manage.py
├── barber_shop/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── appointments/
    ├── __init__.py
    ├── admin.py
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── forms.py
    ├── migrations/
    └── templates/
        └── appointments/
            ├── base.html
            ├── home.html
            ├── registrazione.html
            ├── login.html
            ├── lista_appuntamenti.html
            └── crea_appuntamento.html
```

## Installation

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

3. Install dependencies:
   ```
   pip install django pillow
   ```

4. Create the Django project:
   ```
   django-admin startproject barber_shop .
   ```

5. Create the appointments app:
   ```
   python manage.py startapp appointments
   ```

6. Update `barber_shop/settings.py`:
   - Add `'appointments'` to `INSTALLED_APPS`
   - Set `LANGUAGE_CODE = 'it-it'`
   - Set `TIME_ZONE = 'Europe/Rome'`
   - Add media settings:
     ```
     MEDIA_URL = '/media/'
     MEDIA_ROOT = BASE_DIR / 'media'
     LOGIN_URL = '/login/'
     LOGIN_REDIRECT_URL = '/appuntamenti/'
     ```

7. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

8. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

9. Run the server:
   ```
   python manage.py runserver
   ```

10. Access the admin panel at `http://localhost:8000/admin/` to add barbers and services.

## Usage

- **Home**: View barbers and services, register or login.
- **Registration**: Create a new client account.
- **Login**: Authenticate as a client.
- **Appointments**: List, create, edit, or cancel appointments with filtering.
- **API**: JSON endpoint for available time slots: `/api/slot-disponibili/?data=YYYY-MM-DD&barbiere=ID`

## Populating Sample Data

Run the populate script to add sample clients, barbers, services, and photos:
```
python scripts/populate_data.py
```

## Testing GET and POST

- **GET with filters**: Visit `/appuntamenti/?data=2025-10-15&barbiere=1&stato=confermato`
- **POST for appointments**: Use the form at `/appuntamenti/nuovo/`

## Features

- User registration and authentication
- Appointment booking with time slot selection
- Filtering appointments by date, barber, status
- Admin panel for managing barbers and services
- Responsive templates with Italian localization

## Requirements

- Django==4.2.7
- Pillow==10.1.0

For more details, refer to the code in the respective files.
