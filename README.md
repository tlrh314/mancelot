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
- Docker version 19.03.12, build 48a66213fe
- docker-compose version 1.26.2, build eefe0d31

## Mattermost
- Fetched from: `https://github.com/mattermost/mattermost-docker`
