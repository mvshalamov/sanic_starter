Starter for sanic

Basic software:
 - Sanic
 - asyncpg
 
An environment starting:
 - docker exec -ti sanicstarter_api_1 bash
 - python manage.py runserver
 
Migrations starting:
 - yoyo apply --database postgres://user:dbpass@pg/db ./migrations/migrations -b
 
Tests starting:
 - pytest