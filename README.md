# Task API

A CRUD REST API for managing a to-do list, built with Python, FastAPI, PostgreSQL, and Docker Compose.

## Features

- Create tasks
- Retrieve all tasks
- Retrieve a task by ID
- Update tasks
- Delete tasks
- PostgreSQL database persistence
- Automatic database and table creation
- Automatic seeding of initial tasks
- Parameterized SQL queries
- Input validation
- Health check endpoint
- Correct HTTP status codes for all operations
- Interactive API documentation with Swagger UI
- Dockerized API and database
- Persistent storage using Docker volumes

## Tech Stack

- Python 3.14+
- FastAPI
- Uvicorn
- Pydantic
- PostgreSQL 18
- Psycopg 3
- Docker
- Docker Compose

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/pbword/task-crud-fastapi.git
cd task-crud-fastapi
```

### 2. Configure environment variables

Create a `.env` file in the project root, or copy the provided example:

```bash
cp .env.example .env
```

Configure the following variables:

```env
DATABASE_URL=postgresql://postgres:dev@localhost:5432/tasks
POSTGRES_PASSWORD=dev
```

The password `dev` is intended for local development only.

When running through Docker Compose, the API connects to PostgreSQL using the internal hostname `db` instead of `localhost`.

### 3. Start the application using Docker Compose

Make sure Docker Engine is running, then execute:

```bash
docker compose up --build
```

Docker Compose automatically:

- Builds the FastAPI application image
- Starts the PostgreSQL container
- Waits for PostgreSQL to become healthy
- Starts the FastAPI application
- Initializes the database table and seeds initial tasks if the table is empty

The API will be available at:

http://localhost:8000

### 4. Stop the application

```bash
docker compose down
```

The PostgreSQL database persists through a Docker named volume, so existing tasks remain available when the containers are restarted.

**Note:** Running `docker compose down -v` also removes the database volume and its stored data.

## Run Locally (Without Dockerizing the API)

You can also run FastAPI directly using Python, provided PostgreSQL is already running and accessible.

### 1. Create a virtual environment

```bash
python3 -m venv .venv
```

### 2. Activate the virtual environment

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the development server

```bash
python -m uvicorn main:app --reload
```

The API will be available at:

http://localhost:8000

## Environment Variables

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string used by FastAPI |
| `POSTGRES_PASSWORD` | Password for the PostgreSQL database |

The `.env` file is excluded from version control using `.gitignore`. An `.env.example` file is provided as a configuration reference.

Docker Compose overrides `DATABASE_URL` inside the API container to connect to the `db` service.

## API Documentation

FastAPI automatically generates interactive Swagger UI documentation.

Open:

http://localhost:8000/docs

You can use Swagger UI to test all API endpoints directly from your browser.

![Swagger UI](swagger-ui.png)

## Endpoints

| Method | Endpoint | Description | Success Status |
|---|---|---|---|
| GET | `/` | Get API information | 200 |
| GET | `/health` | Health check | 200 |
| GET | `/tasks` | Get all tasks | 200 |
| GET | `/tasks/{id}` | Get a task by ID | 200 |
| POST | `/tasks` | Create a new task | 201 |
| PUT | `/tasks/{id}` | Update an existing task | 200 |
| DELETE | `/tasks/{id}` | Delete an existing task | 204 |

The API also returns appropriate error responses, including `400 Bad Request`, `404 Not Found`, and validation errors.

## Example Task

```json
{
  "id": 1,
  "title": "Learn FastAPI",
  "done": false
}
```

## Data Storage

PostgreSQL is used to provide persistent relational storage for the application.

Unlike the previous SQLite implementation, PostgreSQL runs as a separate database service managed through Docker Compose.

The database and `tasks` table are created automatically when the application starts if they do not already exist.

If the table is empty, three initial tasks are automatically inserted.

The database uses the following structure:

| Column | Type | Description |
|---|---|---|
| `id` | SERIAL | Auto-incrementing primary key |
| `title` | TEXT | Task title, cannot be NULL |
| `done` | BOOLEAN | Completion status, defaults to FALSE |

Database operations use Psycopg 3 with parameterized SQL queries.

PostgreSQL stores its data in a Docker named volume (`taskdata`), ensuring that records persist across container restarts.

## PostgreSQL Database

The database can be inspected directly using PostgreSQL's `psql` command-line client.

Connect to the PostgreSQL container:

```bash
docker compose exec db psql -U postgres -d tasks
```

Display the available tables:

```sql
\dt
```

Retrieve all tasks:

```sql
SELECT * FROM tasks;
```

Retrieve a specific task:

```sql
SELECT * FROM tasks WHERE id = 2;
```

The screenshot below shows the PostgreSQL database and stored task records.

![PostgreSQL Database](postgres-database.png)

## Testing

The API can be tested using Swagger UI or directly from the command line with `curl`.

### Swagger UI

Open:

http://localhost:8000/docs

### curl

Get all tasks:

```bash
curl -i http://localhost:8000/tasks
```

Get a task by ID:

```bash
curl -i http://localhost:8000/tasks/1
```

Create a task:

```bash
curl -i -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn FastAPI"}'
```

Update a task:

```bash
curl -i -X PUT http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"done": true}'
```

Delete a task:

```bash
curl -i -X DELETE http://localhost:8000/tasks/1
```

### Example Request

```bash
curl -i -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Test PostgreSQL with curl"}'
```

### Example Response

A successful request returns `201 Created` with a JSON response containing the newly created task.

```http
HTTP/1.1 201 Created
date: Tue, 10 Nov 2026 15:44:27 GMT
server: uvicorn
content-length: 57
content-type: application/json

{"id":6,"title":"Test PostgreSQL with curl","done":false}

## Database Persistence

PostgreSQL data is stored in a persistent Docker volume.

To verify persistence:

1. Create a new task using the API.
2. Stop the containers using `docker compose down`.
3. Restart them using `docker compose up`.
4. Retrieve the tasks using `GET /tasks`.

The newly created task should still be present after restarting the containers.