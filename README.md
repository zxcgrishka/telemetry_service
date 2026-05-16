# Telemetry Service

[Русская версия (Russian)](README_ru.md)

RESTful API service to collect telemetry data from devices and asynchronously process analytics.

## Key Features
- **Full JWT Authentication:** Access and Refresh tokens for secure sessions.
- **UUID Identifiers:** Devices use industry-standard UUIDs instead of simple integers.
- **Async Analytics:** Heavy metric calculations performed in the background using Celery and Redis.
- **Paginated Data:** High-performance telemetry retrieval with limit/skip and time filtering.

## Technology Stack
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **Task Queue:** Celery with Redis
- **Containerization:** Docker & Docker Compose
- **Load Testing:** Locust

## Project Structure
- `app/`: Main application code
  - `main.py`: FastAPI entry point and router integration.
  - `models.py`: SQLAlchemy database models (PostgreSQL).
  - `schemas.py`: Pydantic data schemas (DTO pattern).
  - `crud.py`: Database operations (Create, Read, Update, Delete).
  - `worker.py`: Celery tasks and background configuration.
  - `config.py`: Application settings and environment variables management.
  - `database.py`: DB engine setup and session management.
  - `deps.py`: FastAPI dependencies (JWT authentication).
  - `security.py`: Security utilities (JWT creation, password hashing).
  - `routers/`: API endpoints grouped by resource (Users, Devices, etc.).
- `alembic/`: Database migration scripts and environment.
- `alembic.ini`: Configuration for Alembic migrations.
- `Dockerfile` & `docker-compose.yml`: Docker orchestration and container setup.
- `pyproject.toml` & `poetry.lock`: Python dependencies and project metadata.
- `locustfile.py`: Load testing scenario script.
- `locust_report.html`: Detailed HTML report of the latest load test.

## How to Run

### Using Docker (Recommended)
1. Ensure Docker and Docker Compose are installed and running.
2. Run the following command:
   ```bash
   docker-compose up --build
   ```
3. The API will be available at `http://localhost:8080`.
4. Interactive API documentation (Swagger UI) is available at `http://localhost:8080/docs`.

### Local Development (without Docker)
1. Install dependencies using Poetry:
   ```bash
   poetry install
   ```
2. Set up PostgreSQL and Redis.
3. Configure environment variables (export them or set in your environment). 
   **Note:** For production deployment, it is highly recommended to move all sensitive data (passwords, secret keys) to a `.env` file and exclude it from version control.
   ```
   DATABASE_URL=postgresql+asyncpg://user:pass@localhost/telemetry
   SYNC_DATABASE_URL=postgresql://user:pass@localhost/telemetry
   REDIS_URL=redis://localhost:6379/0
   ```
4. Run migrations:
   ```bash
   poetry run alembic upgrade head
   ```
5. Start the FastAPI server:
   ```bash
   poetry run uvicorn app.main:app --reload --port 8080
   ```
6. Start the Celery worker:
   ```bash
   poetry run celery -A app.worker.celery worker --loglevel=info
   ```

## API Endpoints

### Users & Auth
- `POST /users/`: Register a new user.
- `POST /users/login`: Get Access and Refresh tokens.
- `POST /users/refresh`: Renew Access token using Refresh token.

### Devices
- `GET /devices/`: List all devices for the current user.
- `POST /devices/`: Register a new device (UUID generated automatically).

### Telemetry Collection
- `GET /telemetry/{device_id}`: Retrieve history with pagination and time filters.
- `POST /telemetry/{device_id}`: Receive telemetry data (`x`, `y`, `z`).

### Analytics
- `POST /analytics/device/{device_id}`: Trigger device analysis. Returns `task_id`.
- `POST /analytics/user/{user_id}`: Trigger analysis for all user's devices.
- `GET /analytics/task/{task_id}`: Check status and get results (min, max, median, etc.).

## Load Testing
Results are saved in `locust_report.html`. To run manually:
1. Start the service.
2. Run `poetry run locust`.
3. Open `http://localhost:8089`.
