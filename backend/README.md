## **Dependencies**
- Python 3.7.4
- Django 2.2.4
- See and intall `requirements.txt` for full dependencies

## **Installation for development, e.g. using a virtualenv**
- Create virtualenvironment: `virtualenv venv`
- Activate virtualenv: `source venv/bin/activate`

- Install required packages: `pip install -r requirements.txt`
- Setup local settings: `cp settings/.env.example settings/.env`
- Edit `settings/.env` to tailor to your machine.

- `python manage.py check`
- `python manage.py migrate`
- `python manage.py createsuperuser`
- When using `SITE_ID = 1` in the settings module one must make sure that the 
  Site with id=1 exists. So first we delete all existing sites, then create
  one for localhost.
- `python manage.py shell -c 'from django.contrib.sites.models import Site; Site.objects.all().delete(); Site.objects.create(id=1, name="localhost:8000", domain="localhost:8000")'`

## **Running with Docker**
- Build the image: `docker build -t mancelot .`

- Run the built-in Django development server: `docker run --rm -it -v "$(pwd)":/mancelot -p 8000:1337 --name runserver mancelot bash -c "python manage.py runserver 0.0.0.0:1337"`
- In a new terminal, one can attach to the `runserver` container in an interactive session: `docker exec -it runserver bash`
- Website runs on http://localhost:8000 (NB, must accept self-signed certificate)
- Or to run with nginx + uwsgi
  - in the parent folder: `docker-compose up --build -d nginx`
  - in this folder: `docker-compose up -d django` (or omit `django` to start all services, e.g. to develop tasks)
- In a new terminal, one can attach to the `django` container in an interactive session: `docker exec -it mancelot-django bash`
- Website runs on https://localhost (NB, must accept self-signed certificate)

### Add the initial data to the database
- TODO: `python manage.py loaddata fixtures/filename.json` 
- For example: `python manage.py shell -c "from catalogue.factories import *; ProductFactory.create_batch(100)"`

