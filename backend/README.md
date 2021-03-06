## **Dependencies**
- Python 3.9.2
- Django 3.1.7
- See and install `requirements.txt` for full dependencies

## **Database schema**
![Database schema for catalogue and accounts](https://github.com/tlrh314/mancelot/edit/master/backend/mancelot_db.png)

## **Resources**


- The endpoints for the `accounts` and `catalogue` apps are registered and hyperlinked
in the `BrowsableAPI` root.  Details can intuitively be explored there. NB, all
`catalogue` resources are `GET` only and require an authenticated user.
  - `GET` [https://api.mancelot.app/api/v1/](https://api.mancelot.app/api/v1/)


- `accounts.models.UserModel` endpoints. Note that `<pk>=me` returns `request.user`
  - `GET` [https://api.mancelot.app/api/v1/users](https://api.mancelot.app/api/v1/users), permissions = `IsAdmin`
  - `POST` [https://api.mancelot.app/api/v1/users](https://api.mancelot.app/api/v1/users), permissions = `AllowAny`
  - `GET` [https://api.mancelot.app/api/v1/users/\<pk>](https://api.mancelot.app/api/v1/users/me), permissions = `IsAdminOrSelf`
  - `PUT` [https://api.mancelot.app/api/v1/users/\<pk>](https://api.mancelot.app/api/v1/users/me), permissions = `IsAdminOrSelf`
  - `PATCH` [https://api.mancelot.app/api/v1/users/\<pk>](https://api.mancelot.app/api/v1/users/me), permissions = `IsAdminOrSelf`
  - `DELETE` [https://api.mancelot.app/api/v1/users/\<pk>](https://api.mancelot.app/api/v1/users/me), permissions = `IsAdmin`

  - `GET` [https://api.mancelot.app/api/v1/users/\<pk>/favorites](https://api.mancelot.app/api/v1/users/me/favorites), permissions = `IsAdminUserOrSelf`
  - `PATCH` [https://api.mancelot.app/api/v1/users/\<pk>/favorites](https://api.mancelot.app/api/v1/users/me/favorites), permissions = `IsAdminUserOrSelf`
  - `DELETE` [https://api.mancelot.app/api/v1/users/\<pk>/favorites](https://api.mancelot.app/api/v1/users/me/favorites), permissions = `IsAdminUserOrSelf`


#### Additional auth resources that are not listed in the `BrowsableAPI` root

- Obtain a [JSON Web Token](https://github.com/davesque/django-rest-framework-simplejwt)
  for usage of the Mancelot API
  - `POST` [https://api.mancelot.app/api/v1/auth/jwtoken/](https://api.mancelot.app/api/v1/auth/jwtoken/)
      - Use the `access` token obtained in the response **in each consecutive** request
      by using the request header `Authorization: Bearer token`
      - See `settings/base.py` for the value of `SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]`
      for the lifetime of the access token.
  - `POST` [https://api.mancelot.app/api/v1/auth/jwtoken/refresh/](https://api.mancelot.app/api/v1/auth/jwtoken/refresh/)
      - See `settings/base.py` for the value of `SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"]`
      for the lifetime of the refresh token.
  - `POST` [https://api.mancelot.app/api/v1/auth/jwtoken/verify/](https://api.mancelot.app/api/v1/auth/jwtoken/verify/)

- Authentication using Django's built-in session backend (e.g. for the BrowsableAPI)
  - [https://api.mancelot.app/api/v1/auth/login/](https://api.mancelot.app/api/v1/auth/login/)
  - [https://api.mancelot.app/api/v1/auth/logout/](https://api.mancelot.app/api/v1/auth/logout/)


## **Django admin**
- [https://api.mancelot.app/admin/](https://api.mancelot.app/admin/)

## **Installation for development, e.g. using a virtualenv, optie 1**
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
### Optie 2a
- Build the image /w [BuildKit](https://stackoverflow.com/a/58021389): `DOCKER_BUILDKIT=1 docker build -t mancelot_django .`

- Run the built-in Django development server: `docker run --rm -it -v "$(pwd)":/mancelot -p 8000:1337 --name runserver mancelot_django bash -c "python manage.py runserver 0.0.0.0:1337"`
- In a new terminal, one can attach to the `runserver` container in an interactive session: `docker exec -it runserver bash`
- Website runs on http://localhost:8000

### Optie 2b
- Or to run with nginx + uwsgi
  - in the `../nginx` folder: `docker-compose -p mancelot up --build -d nginx`
  - in this folder: `docker-compose -p mancelot up -d django` (or omit `django` to start all services, e.g. to develop tasks)
- In a new terminal, one can attach to the `django` container in an interactive session: `docker exec -it mancelot_django_1 bash`
- Website runs on https://localhost (NB, must accept self-signed certificate)

### Add the initial data to the database
- TODO: `python manage.py loaddata fixtures/filename.json`
- For example: `python manage.py shell -c "from catalogue.factories import *; ProductFactory.create_batch(100)"`


## Django comands
- Create translations dictionaries: `python manage.py makemessages --locale en --locale nl`
  - when used, please **update the translation dictionaries** in `locale/*/*/*.po`, then add/commit/push to repository
- Compile translations dictionaries; `python manage.py compilemessages` (also lives in `entrypoint.sh`)
- Create migrations: `python manage.py makemigrations`
  - when used, please add/commit/push to repository
- Run migrations: `python manage.py migrate` (also lives in `entrypoint.sh`)
- Collect static: `python manage.py collectstatic --noinput` (also lives in `entrypoint.sh`)

## Interaction with the API

- Create new user

```bash
new_user=$(curl -s -k -X POST -H 'Content-Type: application/json' -d '{"email": "timo@halbesma.com", "password": "secret123"}' "https://localhost/api/v1/users")
echo $new_user | jq

```

- Retrieve favorites

```bash
token=$(curl -s -k -X POST -H 'Content-Type: application/json' -d '{"email": "timo@halbesma.com", "password": "secret123"}' "https://localhost/api/v1/auth/jwtoken/" | jq -r '.access')
favorites=$(curl -s -H "Authorization: Bearer ${token}" -k -X GET https://localhost/api/v1/users/me/favorites)
echo $favorites | jq
```
