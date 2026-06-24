.PHONY: dev prod migrate seed shell test check clean

dev:
	python manage.py runserver 0.0.0.0:8000

prod:
	gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4

migrate:
	python manage.py migrate

seed:
	python manage.py seed_tasks
	python manage.py seed_data
	python manage.py create_admin

shell:
	python manage.py shell

test:
	python manage.py test website --verbosity=2

check:
	python manage.py makemigrations --check --dry-run
	python manage.py check --deploy

clean:
	find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name '*.pyc' -delete
