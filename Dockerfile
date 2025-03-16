ARG PYTHON_VERSION=3.12.8
FROM python:${PYTHON_VERSION}-slim AS base

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry install --only main --no-interaction --no-root

COPY static /app/static
COPY . .


CMD ["python", "run.py"]
