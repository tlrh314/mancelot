.PHONY: all $(MAKECMDGOALS)

SHELL=/bin/bash

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help


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
	docker build -f backend/Dockerfile -t mancelot-django backend

django-start:  ## Start Django
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
	echo $$DB_HOST
	DB_NAME=$$(docker exec mancelot_django_1 python manage.py shell -c \
		"from django.conf import settings; print(settings.DATABASES['default']['NAME'])"); \
	DB_USER=$$(docker exec mancelot_django_1 python manage.py shell -c \
		"from django.conf import settings; print(settings.DATABASES['default']['USER'])"); \
	DB_PASSWORD=$$(docker mancelot_django_1 python manage.py shell -c \
		"from django.conf import settings; print(settings.DATABASES['default']['PASSWORD'])"); \
	\
	mysqldump --protocol TCP -h$$DB_HOST -u$$DB_USER --password=$$DB_PASSWORD $$DB_NAME > \
		/data/backups/sqldumps/$${TODAY}/$${DB_NAME}_$${TODAY}.sql; \
	ls -lah $${MANCELOT_DATA_PATH-./data/}/sqldumps/$$TODAY/$${DB_NAME}_$${TODAY}.sql; \


preact:  ## Build Preact (frontend)
	@cd frontend; \
	npm install; \
	npm run build; \
	cd ..


stop: ## Stop and remove a running container, given its name.
	docker stop $(APP_NAME); docker rm $(APP_NAME)

# NEVER EXECUTE THIS COMMAND IN PRODUCTION
quit: ## Stop and remove all running containers.
	@if [[ $$HOSTNAME == "ChezTimo15"* ]]; then  \
		docker stop $$(docker ps -a -q); docker rm $$(docker ps -a -q); \
	else  \
		echo "For safety not implemented for hostname on $$HOSTNAME"; \
	fi
