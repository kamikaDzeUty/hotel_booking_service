#Dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry \
 && poetry config virtualenvs.create false \
 && poetry install --with dev --no-interaction --no-ansi

COPY . .

CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]
