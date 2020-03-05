.PHONY: all $(MAKECMDGOALS)

SHELL=/bin/bash

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help


docker-pull:  ## Pull the latest Docker images from Dockerhub
	docker pull python:3.7-slim-buster
	docker pull certbot/certbot:latest
	docker pull redis:alpine
	docker pull nginx:1.17-alpine
	docker pull mariadb:10.4
	docker pull postgres:9.4-alpine


nginx:  ## Build container for nginx
	docker-compose -f nginx/docker-compose.yml build

nginx-start:  ## Start nginx
	docker-compose -p mancelot -f nginx/docker-compose.yml up --build -d

nginx-stop:  ## Stop nginx
	docker-compose -p mancelot -f nginx/docker-compose.yml stop nginx certbot
	docker-compose -p mancelot -f nginx/docker-compose.yml rm -f nginx certbot

nginx-restart:  ## Restart nginx
	git pull
	make nginx
	make nginx-stop
	make nginx-start
	docker image prune -f

nginx-log:  ## Continously monitor log of nginx
	while true; do \
		docker logs -f --tail 1 mancelot_nginx_1; \
		sleep 10; \
	done


django:  ## Build container for Django (backend)
	docker build -f backend/Dockerfile -t mancelot_django backend

django-start:  ## Start Django
	if [ -f backend/celerybeat.pid ]; then rm -f backend/celerybeat.pid; fi;
	docker-compose -p mancelot -f backend/docker-compose.yml up --build -d

django-stop:  ## Stop Django
	docker-compose -p mancelot -f backend/docker-compose.yml stop django celery celery_beat celery_flower
	docker-compose -p mancelot -f backend/docker-compose.yml rm -f django celery celery_beat celery_flower

django-restart:  ## Restart Django
	git pull
	make django
	make django-stop
	make django-start
	docker image prune -f

django-log:  ## Continously monitor log of uWSGI
	while true; do \
		docker logs -f --tail 1 mancelot_django_1; \
		sleep 10; \
	done

django-sqldump:  ## sql dump of the database (e.g. for backups)
	TODAY=$$(date "+%Y%m%d"); \
	mkdir -p $${MANCELOT_DATA_PATH-./data/}/sqldumps/$$TODAY; \
	DB_HOST=$$(docker exec mancelot_django_1 python manage.py shell -c \
		"from django.conf import settings; print(settings.DATABASES['default']['HOST'])"); \
	DB_NAME=$$(docker exec mancelot_django_1 python manage.py shell -c \
		"from django.conf import settings; print(settings.DATABASES['default']['NAME'])"); \
	DB_USER=$$(docker exec mancelot_django_1 python manage.py shell -c \
		"from django.conf import settings; print(settings.DATABASES['default']['USER'])"); \
	DB_PASSWORD=$$(docker exec mancelot_django_1 python manage.py shell -c \
		"from django.conf import settings; print(settings.DATABASES['default']['PASSWORD'])"); \
	\
	docker exec -it mancelot_django_1 bash -c " \
		mysqldump --protocol TCP -h$$DB_HOST -u$$DB_USER --password=$$DB_PASSWORD $$DB_NAME > \
			/sqldumps/$${TODAY}/$${DB_NAME}_$${TODAY}.sql \
	"; \
	ls -lah $${MANCELOT_DATA_PATH-./data/}sqldumps/$$TODAY/$${DB_NAME}_$${TODAY}.sql; \

dev-db-update:  ## download and load sql dump
	@if [[ $$HOSTNAME == "ChezTimo15"* || $$HOSTNAME == "SurfacePro3" ]]; then  \
		TODAY=$$(date "+%Y%m%d"); \
		rsync -auHxv --progress mancelot:~/production/data/sqldumps/ $${MANCELOT_DATA_PATH-./data/}sqldumps/; \
		\
		DB_HOST=$$(docker exec mancelot_django_1 python manage.py shell -c \
			"from django.conf import settings; print(settings.DATABASES['default']['HOST'])"); \
		DB_NAME=$$(docker exec mancelot_django_1 python manage.py shell -c \
			"from django.conf import settings; print(settings.DATABASES['default']['NAME'])"); \
		DB_USER=$$(docker exec mancelot_django_1 python manage.py shell -c \
			"from django.conf import settings; print(settings.DATABASES['default']['USER'])"); \
		DB_PASSWORD=$$(docker exec mancelot_django_1 python manage.py shell -c \
			"from django.conf import settings; print(settings.DATABASES['default']['PASSWORD'])"); \
		\
		docker exec -it mancelot_django_1 bash -c " \
			mysql --protocol TCP -h$$DB_HOST -u$$DB_USER --password=$$DB_PASSWORD $$DB_NAME \
				< /sqldumps/$${TODAY}/$${DB_NAME}_$${TODAY}.sql"; \
	else  \
		echo "For safety not implemented for hostname on $$HOSTNAME"; \
	fi


staging:  ## Build container for Django/staging (backend)
	DOCKERIMAGE=mancelot_staging
	docker build -f ../staging/backend/Dockerfile -t mancelot_staging ../staging/backend

staging-start:  ## Start Django/staging
	docker-compose -p staging -f ../staging/backend/docker-compose.yml up --build -d

staging-stop:  ## Stop Django/staging
	docker-compose -p staging -f ../staging/backend/docker-compose.yml stop django celery celery_beat celery_flower
	docker-compose -p staging -f ../staging/backend/docker-compose.yml rm -f django celery celery_beat celery_flower

staging-restart:  ## Restart Django
	git pull
	make staging
	make staging-stop
	make staging-start
	docker image prune -f

mattermost:  ## Build container for mattermost
	docker-compose -f mattermost/docker-compose.yml build

mattermost-start:  ## Start mattermost
	docker-compose -f mattermost/docker-compose.yml up --build -d

mattermost-stop:  ## Stop mattermost
	docker-compose -f mattermost/docker-compose.yml stop app db
	docker-compose -f mattermost/docker-compose.yml rm -f app db

mattermost-restart:  ## Restart mattermost
	git pull
	make mattermost
	make mattermost-stop
	make mattermost-start
	docker image prune -f


preact:  ## Build Preact (frontend)
	@cd frontend; \
	npm install; \
	npm run build; \
	cd ..


stop: ## Stop and remove a running container, given its name.
	docker stop $(APP_NAME); docker rm $(APP_NAME)

# NEVER EXECUTE THIS COMMAND IN PRODUCTION
quit: ## Stop and remove all running containers.
	@if [[ $$HOSTNAME == "ChezTimo15"* || $$HOSTNAME == "SurfacePro3"  ]]; then  \
		docker stop $$(docker ps -a -q); docker rm $$(docker ps -a -q); \
	else  \
		echo "For safety not implemented for hostname on $$HOSTNAME"; \
	fi
