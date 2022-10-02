SHELL := /bin/bash

local_up:
	docker-compose build
	docker-compose up -d
	docker-compose exec web python manage.py migrate


local_restart:
	docker-compose restart

local_down:
	docker-compose down

local_stop:
	docker-compose stop

test:
	pytest -v

local_shell:
	docker-compose exec web sh

local_create_superuser:
	docker-compose exec web python manage.py createsuperuser

test:
	docker-compose run --rm web sh -c "pytest"