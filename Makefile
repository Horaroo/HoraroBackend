SHELL := /bin/bash

local_up:
	docker-compose -f docker-compose.local.yml build
	docker-compose -f docker-compose.local.yml up -d
	docker-compose -f docker-compose.local.yml exec web python manage.py migrate


local_restart:
	docker-compose -f docker-compose.local.yml restart

local_down:
	docker-compose -f docker-compose.local.yml down

local_stop:
	docker-compose -f docker-compose.local.yml stop

local_shell:
	docker-compose -f docker-compose.local.yml exec web sh

local_create_superuser:
	docker-compose -f docker-compose.local.yml exec web python manage.py createsuperuser

test:
	docker-compose -f docker-compose.local.yml run --rm web sh -c "pytest"
	