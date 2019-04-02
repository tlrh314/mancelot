# Mancelot Dockerised Setup

# Dependencies
- Docker version 18.09.3, build 774a1f4
- docker-compose version 1.23.2, build 1110ad01

## Installation on macOS
### HomeBrew installation
- Install Docker: `brew cask install docker`
- Install docker-compose and docker-machine: `brew install docker-compose docker-machine`
- Start the Docker application, e.g. via SpotLight
- Check that Docker is running (in the command line): `docker ps`

## Installation on Debian 9.8
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


# Deployment
- `docker network create my_network || true`
- `docker-compose up --build -d`


## Deployment of Mattermost
### Add the remote repository using Git subtree
- `git remote add -f mattermost https://github.com/mattermost/mattermost-docker`
- `git subtree add --prefix mattermost mattermost master --squash`
### Pull in remote updates
- `git fetch mattermost master`
- `git subtree pull --prefix mattermost mattermost master --squash`
