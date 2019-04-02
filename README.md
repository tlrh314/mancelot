# PSONO - Quickstart

# Canonical source

The canonical source of PSONO Quickstart is [hosted on GitLab.com](https://gitlab.com/psono/psono-quickstart).

# Preamble
This is the PSONO Quickstart project, intended to spin up a demo or development environment in a few seconds.



# How to Use

### Prerequirements

- Ubuntu 16.04 (Ubuntu 12.04+ LTS and Debian based systems should be similar if not even identical.)
- Docker (Installation guide: [docks.docker.com](https://docs.docker.com/engine/installation/linux/ubuntu/#install-using-the-repository))
- Docker Compose (Installation guide: [docks.docker.com](https://docs.docker.com/compose/install/))
- Manage Docker without root rights (Installation guide: [docks.docker.com](https://docs.docker.com/engine/installation/linux/linux-postinstall/))

### Install

    mkdir -p ~/psono && \
    rm -Rf ~/psono/psono-quickstart && \
    git clone https://gitlab.com/psono/psono-quickstart.git ~/psono/psono-quickstart && \
    ~/psono/psono-quickstart/psono -c installdev
    
### Start the stack
    
The stack is controlled by docker-compose. To start the stack execute the following commands

    cd ~/psono/psono-quickstart && \
    docker-compose up
    
For a full list of all possible commands of docker-compose visit [docs.docker.com](https://docs.docker.com/compose/reference/overview/)

### Login

Afterwards you can login here:

    URL: http://127.0.0.1:1080/
    user: demo
    pass: demo

