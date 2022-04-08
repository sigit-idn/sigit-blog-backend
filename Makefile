up:
	down
	docker-compose up -d

logs:
	docker-compose logs -f

rebuild:
	make down
	docker-compose up -d --build
	
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

make runserver:
	docker-compose exec -it app python manage.py runserver

make freeze:
	docker-compose exec -it app pip freeze 