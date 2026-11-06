# Unique Wellcare Hospital

Unique Wellcare Hospital is a Django-based hospital management website. It provides
patient-facing information, authentication, doctor and department listings, contact
forms, appointment bookings, and symptom-based doctor recommendations.

## Features

- Hospital home, about, doctor, and department pages
- User signup, login, and logout
- Doctor appointment booking
- Contact form
- Smart doctor recommendations based on described symptoms
- Doctor profile images served from the media directory
- Django admin interface
- SQLite database for local development

## Requirements

- Python 3.12 or newer
- pip
- Git (optional)

The pinned Python dependencies are listed in [requirements.txt](requirements.txt).

## Local setup on Windows

Open PowerShell in the project directory:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
```

For deployments, set `DJANGO_SECRET_KEY` in the environment. The development
fallback in `hms/settings.py` must not be used in production.

If PowerShell prevents virtual-environment activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Load sample clinic data

The seed script creates departments, doctors, and synthetic appointment records:

```powershell
python seed_clinic_data.py
```

The generated patient records are fictional and intended for development only.

## Run the development server

```powershell
python manage.py runserver
```

Open <http://127.0.0.1:8000/> in a browser.

Useful routes include:

- `/admin/` - Django administration
- `/doctors/` - Doctor directory
- `/departments/` - Department directory
- `/booking/` - Appointment booking
- `/smart_recommendation/` - Smart doctor recommendation
- `/contact/` - Contact form
- `/profile/` - Authenticated patient profile

Create an admin user when needed:

```powershell
python manage.py createsuperuser
```

## Tests and checks

Run Django's system checks:

```powershell
python manage.py check
```

Run the test suite:

```powershell
python manage.py test
```

## Docker

Build and run the development container:

```powershell
docker build -t unique-wellcare-hospital .
docker run --rm -p 8000:8000 unique-wellcare-hospital
```

Then open <http://127.0.0.1:8000/>.

## Project structure

```text
hms/
├── hms/                 # Django project configuration
├── home/                # Main application
│   ├── models.py        # Departments, doctors, bookings, contacts
│   ├── views.py         # Page and form views
│   ├── recommendations.py
│   ├── templates/
│   └── static/
├── media/               # Uploaded doctor images
├── db.sqlite3           # Local development database
├── manage.py
├── requirements.txt
└── seed_clinic_data.py
```

## Production notes

The current settings are configured for local development (`DEBUG = True`) and
contain a development secret key. Before deployment, move secrets to environment
variables, disable debug mode, configure production hosts, use a production
database, and serve static and media files through a suitable web server.
