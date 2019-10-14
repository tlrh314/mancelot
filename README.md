# Mancelot

| What            |  Why               | Where            | World                                               |
|-----------------|--------------------|------------------|-----------------------------------------------------|
| [nginx](https://nginx.org/en/docs/)           | Webserver          |  `nginx`         | [mancelot.app](https://www.mancelot.app/)             |
| [Django](https://docs.djangoproject.com/en/2.2/)          | Web Framework      |  `backend`       | [mancelot.app/admin](https://www.mancelot.app/admin/) |
| [Django REST](https://www.django-rest-framework.org)          | Django REST Framework      |  `backend`       | [mancelot.app/api/v1](https://www.mancelot.app/api/v1) |
| [Preact](https://preactjs.com/guide/getting-started) | Frontend |  `frontend`       |  |
| [Mattermost](https://docs.mattermost.com)      | Team Communication |  `mattermost`    | [mm.mancelot.app](https://mm.mancelot.app/)           |


## Infrastructure
### Deployment
- `docker network create mancelot || true`
- `docker-compose up --build -d`

### Dependencies
- Docker version 19.03.1, build 74b1e89
- docker-compose version 1.24.1, build 4667896b

## Frontend
### Add the remote repository using Git subtree
- `git remote add -f frontend git@github.com:lorentzs/mancelot.git`
- `git subtree add --prefix frontend frontend master`
### Pull in remote updates
- `git fetch frontend master`
- `git subtree pull --prefix frontend frontend master`


## Mattermost
- Fetched from: `https://github.com/mattermost/mattermost-docker`
