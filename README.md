# PSONO - Postgres 

Master: [![build status](https://images.microbadger.com/badges/image/psono/psono-postgres.svg)](https://hub.docker.com/r/psono/psono-postgres/) [![build status](https://gitlab.com/psono/psono-postgres/badges/master/build.svg)](https://gitlab.com/psono/psono-postgres/commits/master) [![coverage report](https://gitlab.com/psono/psono-postgres/badges/master/coverage.svg)](https://gitlab.com/psono/psono-postgres/commits/master)
Develop: [![build status](https://gitlab.com/psono/psono-postgres/badges/develop/build.svg)](https://gitlab.com/psono/psono-postgres/commits/develop) [![coverage report](https://gitlab.com/psono/psono-postgres/badges/develop/coverage.svg)](https://gitlab.com/psono/psono-postgres/commits/develop)

### Quickstart: Docker Compose

    version: '2'
    services:
      master:
        image: psono/psono-postgres:latest
        environment:
	      - POSTGRES_USER=usernamehere
	      - POSTGRES_PASSWORD=passwordhere
	      - POSTGRES_REPLICATION_USER=replusernamehere
	      - POSTGRES_REPLICATION_PASSWORD=replpasswordhere
	      - POSTGRES_REPLICATION_MODE=master
      volumes:
        - /opt/docker/psono-postgres-master-data:/var/lib/postgresql/data
    
      slave:
        image: psono/psono-postgres:latest
        links:
          - master:master
        environment:
	      - POSTGRES_USER=usernamehere
	      - POSTGRES_PASSWORD=passwordhere
	      - POSTGRES_REPLICATION_USER=replusernamehere
	      - POSTGRES_REPLICATION_PASSWORD=replpasswordhere
	      - POSTGRES_REPLICATION_MODE=slave
	      - POSTGRES_REPLICATION_MASTER_HOST=master
	      - POSTGRES_REPLICATION_MASTER_PORT=5432
      volumes:
        - /opt/docker/psono-postgres-slave-data:/var/lib/postgresql/data

### Environment variables for master:

      - POSTGRES_USER=usernamehere
      - POSTGRES_PASSWORD=passwordhere
      - POSTGRES_REPLICATION_USER=replusernamehere
      - POSTGRES_REPLICATION_PASSWORD=replpasswordhere
      - POSTGRES_REPLICATION_MODE=master


### Environment variables for slave:

      - POSTGRES_USER=usernamehere
      - POSTGRES_PASSWORD=passwordhere
      - POSTGRES_REPLICATION_USER=replusernamehere
      - POSTGRES_REPLICATION_PASSWORD=replpasswordhere
      - POSTGRES_REPLICATION_MODE=slave
      - POSTGRES_REPLICATION_MASTER_HOST=master
      - POSTGRES_REPLICATION_MASTER_PORT=5432

### Production Usage:

On the master server, run this to start the master node:

    docker run --name my-master \
        -e "POSTGRES_USER=usernamehere" \
        -e "POSTGRES_PASSWORD=passwordhere" \
        -e "POSTGRES_REPLICATION_USER=replusernamehere" \
        -e "POSTGRES_REPLICATION_PASSWORD=replpasswordhere" \
        -e "POSTGRES_REPLICATION_MODE=master" \
        -v /opt/docker/psono-postgres:/var/lib/postgresql/data \
        -d --restart=unless-stopped -p 5432:5432 psono/psono-postgres:latest

On the standby host, run this to start the standby host and connect to the master node:

    docker run --name my-slave \
        -e "POSTGRES_USER=usernamehere" \
        -e "POSTGRES_PASSWORD=passwordhere" \
        -e "POSTGRES_REPLICATION_USER=replusernamehere" \
        -e "POSTGRES_REPLICATION_PASSWORD=replpasswordhere" \
        -e "POSTGRES_REPLICATION_MODE=slave" \
        -e "POSTGRES_REPLICATION_MASTER_HOST=IP-OF-MASTER" \
        -e "POSTGRES_REPLICATION_MASTER_PORT=5432" \
        -v /opt/docker/psono-postgres:/var/lib/postgresql/data \
        -d --restart=unless-stopped -p 5432:5432 psono/psono-postgres:latest

### Backup your database:

Best approach is to make the backups from one of the slaves.

	docker exec -t my-slave pg_dumpall -c -U postgres > dump_`date +%d-%m-%Y"_"%H_%M_%S`.sql

or zipped:

    docker exec -t my-slave pg_dumpall -c -U postgres | gzip > dump_`date +%d-%m-%Y"_"%H_%M_%S`.gz

You may want to schedule this command as a cronjob to generate regular backups.

### Restore your database:

To restore a backup, execute the following:

	cat dump_XX-XX-XXXX_XX_XX_XX.sql | docker exec -i my-master psql -U postgres
	
or if it was zipped:

	cat dump_XX-XX-XXXX_XX_XX_XX.gz | gunzip | docker exec -i my-master psql -U postgres

### Test config

    cd 9.6 && docker-compose up -d --build

### Promote a slave to master

    docker exec my-slave touch /tmp/postgresql.trigger.5432

(You still have to update other slaves to recognize this slave as new master)