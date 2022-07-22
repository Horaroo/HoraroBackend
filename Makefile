#.PHONY:local_up local_down
SHELL := /bin/bash

local_up:
	docker-compose build --parallel
	docker-compose up

local_restart:
	docker-compose restart

local_down:
	docker-compose down

local_stop:
	docker-compose stop

test:
	pytest -v

local_shell:
	docker-compose exec web bash

local_create_superuser:
	docker-compose exec web python manage.py createsuperuser