up:
	docker-compose up -d

reup:
	docker-compose up -d --force-recreate

logs:
	docker-compose logs -f

down:
	docker-compose down

sh:
	docker-compose exec -it app sh

psql:
	docker-compose exec -it db psql -U postgres

migrate:
	docker-compose exec -it app python manage.py migrate

makemigrations:
	docker-compose exec -it app python manage.py makemigrations