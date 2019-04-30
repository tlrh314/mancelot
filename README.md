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
- Docker version 18.09.3, build 774a1f4
- docker-compose version 1.23.2, build 1110ad01


### Installation of Docker
#### Development (TLRH) on macOS --> using HomeBrew
- Install Docker: `brew cask install docker`
- Install docker-compose and docker-machine: `brew install docker-compose docker-machine`
- Start the Docker application, e.g. via SpotLight
- Check that Docker is running (in the command line): `docker ps`

#### Production ([TransIP](https://www.transip.nl/cp/), [BladeVPS X1](https://www.transip.nl/vps/)) on Debian 9.8
- Install the [prerequisites](https://docs.docker.com/install/linux/docker-ce/debian/#prerequisites): `sudo apt-get remove docker docker-engine docker.io containerd runc`
- `sudo apt-get install apt-transport-https ca-certificates curl gnupg2 software-properties-common`
- Add Docker's official GPG key
- Add Docker's stable repo to aptitude `sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"`
- Install docker: `sudo apt-get update; $ sudo apt-get install docker-ce docker-ce-cli containerd.io`
- Test: `sudo docker run hello-world`
- Boot on startup: `sudo systemctl enable docker`
- [Install docker-compose](https://github.com/docker/compose/releases) - NB not via aptitude b/c Debian 9.8 has two year old package
  - `sudo curl -L "https://github.com/docker/compose/releases/download/1.23.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`
  - `sudo chmod +x /usr/local/bin/docker-compose`



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
