FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install poetry \
 && poetry config virtualenvs.create false \
 && poetry install --no-root --no-interaction --no-ansi

COPY . /app

EXPOSE 8000

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
