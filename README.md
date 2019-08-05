# Mancelot

| What            |  Why               | Where            | World                                               |
|-----------------|--------------------|------------------|-----------------------------------------------------|
| [nginx](https://nginx.org/en/docs/)           | Webserver          |  `nginx`         | [mancelot.nl](https://www.mancelot.nl/)             |
| [Django](https://docs.djangoproject.com/en/2.2/)          | Web Framework      |  `backend`       | [mancelot.nl/admin](https://www.mancelot.nl/admin/) |
| [Django REST](https://www.django-rest-framework.org)          | Django REST Framework      |  `backend`       | [mancelot.nl/api/v1](https://www.mancelot.nl/api/v1) |
| [Mattermost](https://docs.mattermost.com)      | Team Communication |  `mattermost`    | [mm.mancelot.nl](https://mm.mancelot.nl/)           |
| [Psono](https://doc.psono.com)           | Password Manager   |  `psono`         | [psono.mancelot.nl](https://psono.mancelot.nl/)     |


## Infrastructure
### Deployment
- `docker network create mancelot || true`
- `docker-compose up --build -d`

### Dependencies
- Docker version 19.03.1, build 74b1e89
- docker-compose version 1.24.1, build 4667896b


## Mattermost
### Add the remote repository using Git subtree
- `git remote add -f mattermost https://github.com/mattermost/mattermost-docker`
- `git subtree add --prefix mattermost mattermost master --squash`
### Pull in remote updates
- `git fetch mattermost master`
- `git subtree pull --prefix mattermost mattermost master --squash`


## Psono (tbd)
### Server: psono-server
- `git remote add -f psono-server https://gitlab.com/psono/psono-server.git`
- `git subtree add --prefix psono/psono-server psono-server v1.9.2 --squash`

### Client: psono-client
- `git remote add -f psono-client https://gitlab.com/psono/psono-client.git`
- `git subtree add --prefix psono/psono-client psono-client v1.11.0 --squash`
