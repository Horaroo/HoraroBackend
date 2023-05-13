SHELL := /bin/bash



up:
	docker-compose up

up_and_build:
	docker-compose up -d --build && docker system prune -f

# example: make up_and_build_one_service service=bot
up_and_build_one_service:
	docker-compose up -d --no-deps --build $(service) && docker system prune -f

down:
	docker-compose down

restart:
	docker-compose restart

stop:
	docker-compose stop

start:
	docker-compose start

webshell:
	docker-compose exec web sh




staging_up:
	docker-compose -f docker-compose.staging.yml up

staging_up_and_build:
	docker-compose -f docker-compose.staging.yml up -d --build && docker system prune -f

# example: make up_and_build_one_service service=bot
staging_up_and_build_one_service:
	docker-compose -f docker-compose.staging.yml up -d --no-deps --build $(service) && docker system prune -f

staging_down:
	docker-compose -f docker-compose.staging.yml down

staging_restart:
	docker-compose -f docker-compose.staging.yml restart

staging_stop:
	docker-compose -f docker-compose.staging.yml stop

staging_start:
	docker-compose -f docker-compose.staging.yml start

staging_web_shell:
	docker-compose -f docker-compose.staging.yml exec web sh




local_up:
	docker-compose -f docker-compose.local.yml build
	docker-compose -f docker-compose.local.yml up


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

format:
	isort .
	black .

lint:
	flake8 . --count --show-source --statistics --max-line-length 120
	isort --check .
	black --check