ARG PYTHON_VERSION=3.12.7
FROM python:${PYTHON_VERSION}-slim AS base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Install Poetry, netcat-openbsd and PostgreSQL client
RUN apt-get update && apt-get install -y netcat-openbsd postgresql-client \
    && pip install poetry \
    && apt-get clean

WORKDIR /app

# Copy dependency files for caching
COPY poetry.lock pyproject.toml /app/

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copy the source code into the container
COPY . /app/

# Create a non-privileged user that the app will run under
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Switch to the non-privileged user to run the application
USER appuser

# Expose the port that the application listens on
EXPOSE 5000

# Run the application
ENTRYPOINT ["sh", "/app/entrypoint.sh"]
