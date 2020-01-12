SHELL := /bin/bash

help:
	make -h

collectstatic:
	. venv/bin/activate
	./manage.py collectstatic --noinput

createsuperuser:
	python ./manage.py createsuperuser

functests:
	pytest -k "functional_test.py" --cov=.

journal-today:
	sudo journalctl -b | tac | less

log-nginx:
	tail -n20 /var/log/nginx/error.log

log-psql:
	tail -n20 /var/log/postgresql/postgresql-10-main.log

migrate:
	. venv/bin/activate && ./manage.py migrate

migrations:
	. venv/bin/activate && ./manage.py makemigrations

restart-nginx:
	sudo systemctl restart nginx

restart-psql:
	sudo systemctl restart postgresql

runserver:
	. venv/bin/activate
	python manage.py runserver 127.0.0.1:8000

runserver-plus:
	. venv/bin/activate
	python manage.py runserver_plus 127.0.0.1:8000

tests:
	pytest --cov=.

unittests:
	pytest -k "not functional_test.py" --cov=.
