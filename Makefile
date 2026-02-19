install:
	uv sync --frozen --no-dev

collectstatic:
	uv run python manage.py collectstatic --noinput

migrate:
	uv run python manage.py migrate --noinput

render-start:
	gunicorn task_manager.wsgi:application --bind 0.0.0.0:$$PORT
