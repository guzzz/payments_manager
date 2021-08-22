#!/bin/bash
.PHONY: default
.SILENT:


default:

shell:
	docker-compose stop backend
	docker-compose run --rm --service-ports backend bash

createsuperuser:
	docker-compose run --rm backend python manage.py createsuperuser

migrate:
	docker-compose run --rm backend python manager.py db init
	docker-compose run --rm backend python manager.py db migrate
	docker-compose run --rm backend python manager.py db upgrade

start:
	docker-compose up -d db
	docker-compose up

start_api:
	docker-compose run --rm --service-ports backend

stop:
	docker-compose down

build:
	docker-compose build --force-rm --no-cache --pull

setup:
	docker network create payments_manager_flask_network
	make build
	docker-compose up -d db
	sleep 10
	make migrate
	make start

logs:
	docker-compose logs --follow

tests:
	docker-compose run --rm backend pytest
	make clean
	docker network create payments_manager_flask_network
	make build
	docker-compose up -d queue
	sleep 10
	make stop
	make migrate
	make start

clean:
	make stop
	docker image rm $$(docker image ls -q -f reference=payments_manager_flask)
	docker volume rm $$(docker volume ls -q -f name=payments-manager-flask-db)
	rm -r migrations
	docker network rm payments_manager_flask_network

coverage:
	docker-compose -f docker-compose.yml run --rm --service-ports backend bash -c \
	"coverage run --source='.' manage.py test; \
	coverage report --rcfile=.coveragerc; \
	coverage html --rcfile=.coveragerc"

black:
	docker-compose -f docker-compose.yml run --rm --service-ports backend bash -c \
	"python -m black ."
