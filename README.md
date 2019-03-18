# https://mancelot.nl

## Installation using Docker Compose

The following instructions deploy Mattermost in a production configuration using multi-node Docker Compose set up.

### Requirements

* [docker] (version `1.12+`)
* [docker-compose] (version `1.10.0+` to support Compose file version `3.0`)

### Choose Edition to Install

If you want to install Enterprise Edition, you can skip this section.

To install the team edition, comment out the two following lines in docker-compose.yaml file:
```yaml
args:
  - edition=team
```
The `app` Dockerfile will read the `edition` build argument to install Team (`edition = 'team'`) or Enterprise (`edition != team`) edition.

### Database container
This repository offer a Docker image for the Mattermost database. It is a customized PostgreSQL image that you should configure with following environment variables :
* `POSTGRES_USER`: database username
* `POSTGRES_PASSWORD`: database password
* `POSTGRES_DB`: database name

It is possible to use your own PostgreSQL database, or even use MySQL. But you will need to ensure that Application container can connect to the database (see [Application container](#application-container))

#### AWS
If deploying to AWS, you could also set following variables to enable [Wal-E](https://github.com/wal-e/wal-e) backup to S3 :
* `AWS_ACCESS_KEY_ID`: AWS access key
* `AWS_SECRET_ACCESS_KEY`: AWS secret
* `WALE_S3_PREFIX`: AWS s3 bucket name
* `AWS_REGION`: AWS region

All four environment variables are required. It will enable completed WAL segments sent to archive storage (S3). The base backup and clean up can be done through the following command:
```bash
# Base backup
docker exec mattermost-db su - postgres sh -c "/usr/bin/envdir /etc/wal-e.d/env /usr/bin/wal-e backup-push /var/lib/postgresql/data"
# Keep the most recent 7 base backups and remove the old ones
docker exec mattermost-db su - postgres sh -c "/usr/bin/envdir /etc/wal-e.d/env /usr/bin/wal-e delete --confirm retain 7"
```
Those tasks can be executed through a cron job or systemd timer.

### Application container
Application container run the Mattermost application. You should configure it with following environment variables :
* `MM_USERNAME`: database username
* `MM_PASSWORD`: database password
* `MM_DBNAME`: database name

If your database use some custom host and port, it is also possible to configure them :
* `DB_HOST`: database host address
* `DB_PORT_NUMBER`: database port

If you use a Mattermost configuration file on a different location than the default one (`/mattermost/config/config.json`) :
* `MM_CONFIG`: configuration file location inside the container.

If you choose to use MySQL instead of PostgreSQL, you should set a different datasource and SQL driver :
* `DB_PORT_NUMBER` : `3306`
* `MM_SQLSETTINGS_DRIVERNAME` : `mysql`
* `MM_SQLSETTINGS_DATASOURCE` : `MM_USERNAME:MM_PASSWORD@tcp(DB_HOST:DB_PORT_NUMBER)/MM_DBNAME?charset=utf8mb4,utf8&readTimeout=30s&writeTimeout=30s`
Don't forget to replace all entries (beginning by `MM_` and `DB_`) in `MM_SQLSETTINGS_DATASOURCE` with the real variables values.

If you want to push Mattermost application to **Cloud Foundry**, use a `manifest.yml` like this one (with external PostgreSQL service):

```
---
applications:
- name: mattermost
  docker:
    image: mattermost/mattermost-prod-app
  instances: 1
  memory: 1G
  disk_quota: 256M
  env:
    DB_HOST: database host address
    DB_PORT_NUMBER: database port
    MM_DBNAME: database name
    MM_USERNAME: database username
    MM_PASSWORD: database password

```

### Web server container
This image is optional, you should **not** use it when you have your own reverse-proxy. It is a simple front Web server for the Mattermost app container. If you use the provided `docker-compose.yml` file, you don't have to configure anything. But if your application container is reachable on custom host and/or port (eg. if you use a container provider), you should add those two environment variables :
* `MATTERMOST_HOST`: mattermost application host address
* `MATTERMOST_PORT_NUMBER`: mattermost application HTTP port

If you plan to upload large files to your Mattermost instance, Nginx will need to write some temporary files. In that case, the `read_only: true` option on the `web` container should be removed from your `docker-compose.yml` file.

#### Install with SSL certificate
Put your SSL certificate as `./volumes/web/cert/cert.pem` and the private key that has
no password as `./volumes/web/cert/key-no-password.pem`. If you don't have
them you may generate a self-signed SSL certificate.

### Starting/Stopping Docker

#### Start
If you are running docker with non root user, make sure the UID and GID in app/Dockerfile are the same as your current UID/GID
```
mkdir -p ./volumes/app/mattermost/{data,logs,config,plugins}
chown -R 2000:2000 ./volumes/app/mattermost/
docker-compose start
```

#### Stop
```
docker-compose stop
```

### Removing Docker

#### Remove the containers
```
docker-compose stop && docker-compose rm
```

#### Remove the data and settings of your Mattermost instance
```
sudo rm -rf volumes
```

## Update Mattermost to latest version

First, shutdown your containers to back up your data.

```
docker-compose down
```

Back up your mounted volumes to save your data. If you use the default `docker-compose.yml` file proposed on this repository, your data is on `./volumes/` folder.

Then run the following commands.

```
git pull
docker-compose build
docker-compose up -d
```

Your Docker image should now be on the latest Mattermost version.
