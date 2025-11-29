## Project Structure

```plaintext
/backend
|   |-- main.py                    # Entry point of the FastAPI app
|   |-- env_var                    # Environment variables. This will get variable from the Docker-compose file.
|   |-- pyproject.toml             # Project dependencies
|   |-- README.md                  # Project setup and structure
|   |-- run.sh                     # This will boot up the application
|   |-- Dockerfile                 # Dockerfile for containerization
|   |-- backend_pre_start.py       # Initialization of the Postgres and checking the connection
|   |-- alembic_ini                # Alembic initializer
|-- backend/
|   |-- api/                         # API versioning
|   |   |-- v1/                      # Version 1 of the API
|   |   |   |-- __init__.py          # V1 Route Integrations
|   |   |   |-- data_coordination/
|   |   |   |   |-- controller.py
|   |   |   |   |-- route.py
|   |   |   |-- status/             # To check the status of the service if it is up and running or not     
|   |   |   |   |-- route.py
|   |-- common/                    # Utility functions for the microservice
|   |   |-- helper.py              # Common utility function that would be reused throughout the project
|   |   |-- process_data.py        # Common function that are used to handle data processing
|   |-- config/                    # Configuration management
|   |   |-- __init__.py
|   |   |-- config.py              # to initialize the environment variable configurations
|   |-- core/                      # Common utilities and core functions
|   |   |-- __init__.py
|   |   |-- base_response.py
|   |   |-- logging.conf            # Logging utilities
|   |   |-- exceptions_handlers.py  # Custom exceptions
|   |-- db/                         # Data models (database and Pydantic models)
|   |   |-- __init__.py
|   |   |-- base_class.py
|   |   |-- base.py
|   |   |-- session.py              # Creating a Postgres Connection
|   |-- integrations/               # External service integrations
|   |   |-- __init__.py
|   |   |-- snowflake_clients.py
|   |   |-- databricks_clients.py
|   |-- migration/                  # External service integrations
|   |   |-- versions/               # Has versions to setup the postres server
|   |   |-- env.py                  # Alembic Setup
|   |   |-- script.py.mako
|   |-- models/                     # Data models (database and Pydantic models)
|   |   |-- __init__.py
|   |   |-- transcript_summary.py   # Consists of the models for SQLAlchemy
|   |-- schemas/                    # Data schemas (database and Pydantic models)
|   |   |-- __init__.py
|   |   |-- status.py
|   |   |-- transcript_summary.py   # Keeps all the schemas used in for summaries
|   |   |-- data_coordination.py    # Keeps all the schemas used for the snowflake and other databases
|   |-- tests/                      # stores/keeps all the unit tests for the service
```


## Build and Run

### Prerequisites

- Python 3.8+
- Docker
- Azure CLI (for deployment)