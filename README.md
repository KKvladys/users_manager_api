# User Management REST API

## Overview

REST API project for user management, built with Flask.


## Technologies Used

- **Python**
- **Flask**
- **Postgres**
- **SQLAlchemy**
- **Docker & Docker Compose**
- **Swagger**
- **Poetry**

## User Model

Each user has the following attributes:

- `id` (integer, primary key)
- `name` (string)
- `email` (string, unique)
- `created_at` (datetime, timestamp of creation)

## Installation



### Steps to Run

1. **Clone the repository:**
   ```sh
   git clone https://github.com/KKvladys/users_manager_api.git
   cd user-management-api
   ```
2. **Create a virtual environment and install dependencies:**
   ```sh
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate    # On Windows
   ```
3. **Install dependencies::**
   ```sh
    pip install poetry
    poetry install
   ```

4. **Create a .env file:**
   ```sh
   cp .env.sample .env
    # Edit the .env file with your configurations
   ```
5. **Apply database migrations:**
   ```sh
   flask --app run.py db upgrade
   ```

6. **Run the application:**
   ```sh
   flask --app run.py run
   ```
   The API Documentation will be available at `http://127.0.0.1:5000/docs/`

### Running with Docker

1. **Build the Docker image:**
   ```sh
   docker build -t user-management-api .
   ```
2. **Run the container:**
   ```sh
   docker-compose up
   ```
   The service Documentation will be accessible at `http://localhost:5000/docs/`

## API Endpoints

| Method | Endpoint      | Description              |
|--------|---------------|--------------------------|
| POST   | `/users`      | Create a new user        |
| GET    | `/users`      | Retrieve all users       |
| GET    | `/users/{id}` | Retrieve a specific user |
| PUT    | `/users/{id}` | Update user details      |
| DELETE | `/users/{id}` | Delete a user            |

## Environment Variables

To deploy the application, configure the database and environment variables, then run:

```
ENVIRONMENT=<"develop" or "prod">

DATABASE_SQLITE_URL="sqlite:///users_db.sqlite3"

# PostgreSQL
POSTGRES_DB=users_db
POSTGRES_PORT=5432
POSTGRES_USER=admin
POSTGRES_PASSWORD=password
POSTGRES_HOST=db

```
## Testing
```sh
   python -m pytest
   ```