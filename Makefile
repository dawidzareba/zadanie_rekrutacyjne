up:
	docker compose up --build

down:
	docker compose down --remove-orphans

stop:
	docker compose stop

build:
	docker compose build

shell:
	docker compose run --rm django python manage.py shell_plus --ipython

admin:
	docker compose run --rm django python manage.py createsuperuser

migrations:
	docker compose run --rm django python manage.py makemigrations

migrate:
	docker compose run --rm django python manage.py migrate

test:
	docker compose run --rm django python manage.py test

prod:
	docker compose -f docker-compose.prod.yml up --build

command:
	docker-compose run --rm django python manage.py $(filter-out $@,$(MAKECMDGOALS))

%:
	@: