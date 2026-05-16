# Telemetry Service

RESTful API service to collect telemetry data from devices and asynchronously process analytics.

## Technology Stack
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **Task Queue:** Celery with Redis
- **Containerization:** Docker & Docker Compose
- **Load Testing:** Locust

## Project Structure
- `app/`: Main application code
  - `main.py`: FastAPI entry point
  - `models.py`: SQLAlchemy database models
  - `schemas.py`: Pydantic data schemas
  - `crud.py`: Database operations
  - `worker.py`: Celery tasks and configuration
  - `routers/`: API endpoints grouped by resource
- `alembic/`: Database migrations
- `Dockerfile` & `docker-compose.yml`: Containerization
- `locustfile.py`: Load testing script

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
3. Configure environment variables (create a `.env` file or export them):
   ```
   DATABASE_URL=postgresql+asyncpg://user:pass@localhost/db
   SYNC_DATABASE_URL=postgresql://user:pass@localhost/db
   REDIS_URL=redis://localhost:6379/0
   ```
4. Run migrations:
   ```bash
   poetry run alembic upgrade head
   ```
5. Start the FastAPI server:
   ```bash
   poetry run uvicorn app.main:app --reload
   ```
6. Start the Celery worker:
   ```bash
   poetry run celery -A app.worker.celery worker --loglevel=info
   ```

## API Endpoints

### Users & Devices
- `POST /users/`: Create a new user.
- `POST /devices/`: Register a device and bind it to a user.

### Telemetry Collection
- `POST /telemetry/{device_id}`: Receive telemetry data (`x`, `y`, `z`).

### Analytics
- `POST /analytics/device/{device_id}`: Trigger analysis for a specific device (optional `start_time`, `end_time`). Returns `task_id`.
- `POST /analytics/user/{user_id}`: Trigger analysis for all devices of a user. Returns `task_id`.
- `GET /analytics/task/{task_id}`: Check task status and get results (min, max, count, sum, median).

## Load Testing
To run load tests with Locust:
1. Ensure the service is running.
2. Start Locust:
   ```bash
   poetry run locust
   ```
3. Open `http://localhost:8089` in your browser and start the test.
