# Makefile
COMPOSE_FILE := docker/docker-compose.yml
ENV_FILE := .env
DC := docker compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE)

.PHONY: build up collectstatic logs start dev

build:
	$(DC) up -d --build

up:
	$(DC) up -d

collectstatic:
	$(DC) run --rm web python manage.py collectstatic --noinput

logs:
	$(DC) logs --tail=200 -f web

start: build collectstatic

dev: start logs
