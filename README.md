
## Setup Process
### Step 1: Navigate to project directory on your local system and build the containers
Below command will build all the necessary docker containers
```python
sh build_all.sh
```
### Step 2: Wait for the docker images to be pulled/build.
### Step 3: Start the containers 🏁
```python
sh start_all.sh
```

## Maintenance 🛠
### Application logs 📝
We use python native logging mechanism. For application level logs run
```python
tail -f logs/debug.logs
```

### Docker logs 📊
Run below command to get docker logs
```python
docker-compose logs -f
```
### Clean-up 🧴
Run below command to bring down all the Docker containers
```python
sh stop_all.sh
```
### Restart 🏁
Run below command to restart all your docker containers
```python
sh restart_all.sh
```

## Project Structure

```plaintext
/{project-name}
|   |-- docker-compose.yaml             # Setup all the three microservices and postgres environment
|   |-- postgresql.conf                 # Contains postgres configurations
|   |-- build_all.sh                    # Commands to build all microservices
|   |-- restart_all.sh                  # Commands to stop and start all microservices
|   |-- start_all.sh                    # Commands to start all microservices
|   |-- stop_all.sh                     # Commands to stop all microservices
|   /{microservice}
|   |   |-- main.py                    # Entry point of the FastAPI app
|   |   |-- env_var                    # Environment variables. This will get variable from the Docker-compose file.
|   |   |-- pyproject.toml             # Project dependencies
|   |   |-- README.md                  # Project setup and structure
|   |   |-- run.sh                     # This will boot up the application
|   |   |-- Dockerfile                 # Dockerfile for containerization
|   |   |-- backend_pre_start.py       # Initialization of the Postgres and checking the connection
|   |   |-- alembic_ini                # Alembic initializer
|   |-- {microservice_name}/
|   |   |-- api/                         # API versioning
|   |   |   |-- v1/                      # Version 1 of the API
|   |   |   |   |-- __init__.py          # V1 Route Integrations
|   |   |   |   |-- {microservice_routes}/
|   |   |   |   |   |-- controller.py
|   |   |   |   |   |-- route.py
|   |   |   |   |-- status/             # To check the status of the service if it is up and running or not     
|   |   |   |   |   |-- route.py
|   |   |-- common/                    # Utility functions for the microservice
|   |   |-- config/                    # Configuration management
|   |   |   |-- __init__.py
|   |   |   |-- config.py              # to initialize the environment variable configurations
|   |   |-- core/                      # Common utilities and core functions
|   |   |   |-- __init__.py
|   |   |   |-- base_response.py
|   |   |   |-- logging.conf            # Logging utilities
|   |   |   |-- exceptions_handlers.py  # Custom exceptions
|   |   |-- db/                         # Include DB connections and session creations
|   |   |-- integrations/               # External service integrations
|   |   |-- migration/                  # External service integrations
|   |   |   |-- versions/               # Has versions to setup the postres server
|   |   |   |-- env.py                  # Alembic Setup
|   |   |   |-- script.py.mako
|   |   |-- models/                     # Data models (database and Pydantic models)
|   |   |-- schemas/                    # Data schemas (database and Pydantic models)
|   |   |-- tests/                      # stores/keeps all the unit tests for the service
```


## Build and Run

### Prerequisites

- Python 3.8+
- Docker