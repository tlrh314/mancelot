# Mancelot

| What            |  Why               | Where            | World                                               |
|-----------------|--------------------|------------------|-----------------------------------------------------|
| [nginx](https://nginx.org/en/docs/)           | Webserver          |  `nginx`         | [mancelot.app](https://www.mancelot.app/)             |
| [Django](https://docs.djangoproject.com/en/2.2/)          | Web Framework      |  `backend`       | [mancelot.app/admin](https://www.mancelot.app/admin/) |
| [Django REST](https://www.django-rest-framework.org)          | Django REST Framework      |  `backend`       | [mancelot.app/api/v1](https://www.mancelot.app/api/v1) |
| [Mattermost](https://docs.mattermost.com)      | Team Communication |  `mattermost`    | [mm.mancelot.app](https://mm.mancelot.app/)           |


## Infrastructure
### Deployment
- `docker network create mancelot || true`
- `docker-compose up --build -d`

### Dependencies
- Docker version 19.03.8, build afacb8b7f0
- docker-compose version 1.25.5, build 8a1c60f6

## Mattermost
- Fetched from: `https://github.com/mattermost/mattermost-docker`
