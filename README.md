
<div align="center">

[![Python 3.14](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/downloads/release/python-314/) [![Robyn](https://img.shields.io/badge/robyn-0.84-blue)](https://robyn.tech/) [![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv) [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) [![Type checked: ty](https://img.shields.io/badge/types-ty-blue)](https://github.com/astral-sh/ty) [![Docker](https://img.shields.io/badge/docker-ready-2496ED)](https://www.docker.com/) [![Pydantic](https://img.shields.io/badge/pydantic-v2-red)](https://docs.pydantic.dev/) [![Structlog](https://img.shields.io/badge/structlog-25.0-lightgrey)](https://www.structlog.org/) [![SQLAlchemy](https://img.shields.io/badge/sqlalchemy-2.0-orange)](https://www.sqlalchemy.org/) [![License: MIT](https://img.shields.io/badge/license-MIT-green)](https://opensource.org/licenses/MIT)

</div>

<div align="center">

# 🕵️ Robyn Crime API
Extended Robyn app example.

Async REST API for managing crime records.
Built with Robyn, Clean Architecture, production-ready tooling.

</div>

---

## 📋 Table of Contents
- [Features](#features)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Architecture](#architecture)
- [Logging System](#logging-system)
- [Configuration](#configuration)
- [Development](#development)
- [License](#license)

---

<a id="features"></a>
## ✨ Features

- **Crime Record Management**:
  - Create, read, update, and delete crime records
  - Paginated listing with configurable skip/limit
  - Full request/response validation with Pydantic v2
  - Structured error responses with request tracing

- **Async & High Performance**:
  - Async Python web server (Robyn + Actix Rust runtime)
  - Async database operations (SQLAlchemy + aiosqlite)
  - WAL-mode SQLite with performance tuning
  - Request duration tracking in nanoseconds

- **Clean Architecture**:
  - Strict separation of concerns (Domain, Database, Endpoints, Config)
  - Repository pattern with pure async functions
  - DI/IoC container with lazy loading and request-scoped providers
  - Interface-based design with adapter pattern

- **Enterprise Logging**:
  - Structured logging with `structlog`
  - JSON output for production, colored console for development
  - Context binding with automatic `request_id` injection
  - File rotation with size limits
  - Third-party logger hijacking (SQLAlchemy, Robyn, Pydantic, etc.)

- **Production Ready**:
  - Full type hints with Python 3.14
  - Ruff for linting and formatting (all rules enabled)
  - `ty` for strict type checking
  - Multi-stage Dockerfile with non-root user
  - Health check endpoint
  - CORS configuration
  - Bearer token authentication (extensible)

---

<a id="quick-start"></a>
## 🚀 Quick Start

### Prerequisites
- Python 3.14+
- [uv](https://github.com/astral-sh/uv)
- Docker (optional)

### Installation

```bash
# Clone the repository
git clone https://github.com/script-logic/robyn-app-example-extended.git
cd robyn_app_example_extended

# Install with uv
uv sync
```

### Run the Server

```bash
# Start the server
uv run python -m robyn_example

# Using Docker
docker-compose up

# Using Just
just run
```

The API will be available at `http://127.0.0.1:8082`.

---

<a id="project-structure"></a>
## 📁 Project Structure

```
├── local_database/                       # SQLite database (WAL mode)
│   └── database.db
├── logs/                                 # Application logs (rotating)
├── src/
│   └── robyn_example/
│       ├── adapters/                     # Adapter layer
│       │   └── adapters.py               # Config → LoggerConfig adapter
│       ├── config/                       # Configuration
│       │   ├── models/                   # Settings models
│       │   │   ├── application_settings.py
│       │   │   ├── cors_settings.py
│       │   │   ├── database_settings.py
│       │   │   ├── filesystem_settings.py
│       │   │   └── logger_settings.py
│       │   └── app_config.py             # Pydantic-settings root
│       ├── database/                     # Database layer
│       │   ├── crime_repository.py       # Pure async repository functions
│       │   ├── db_manager.py             # Engine & session management
│       │   └── models.py                 # SQLAlchemy 2.0 ORM models
│       ├── di/                           # Dependency Injection
│       │   ├── _proxy_ioc.py             # Lazy-loaded proxy container
│       │   └── _real_ioc.py              # Real DI container
│       ├── domain/                       # Domain entities
│       │   └── entities.py               # CrimeEntity, RequestMiddlewareEntity
│       ├── logger/                       # Structured logging system
│       │   ├── handlers.py               # Console & file handlers
│       │   ├── interfaces.py             # LoggerConfig dataclass
│       │   ├── processors.py             # Log processors & cleaners
│       │   ├── renderers.py              # JSON & console renderers
│       │   └── setup.py                  # Logging initialization
│       ├── robyn/                        # Web layer
│       │   ├── endpoints/
│       │   │   ├── api_v1/               # API v1 endpoints
│       │   │   │   ├── endpoints.py      # CRUD route handlers
│       │   │   │   ├── enums.py          # Path parameter enums
│       │   │   │   └── schemas.py        # Request/response schemas
│       │   │   ├── exceptions/           # Error handling
│       │   │   │   ├── exceptions_handler.py
│       │   │   │   └── schemas.py        # Error response models
│       │   │   ├── helpers/              # Parsers & policies
│       │   │   └── health.py             # Health check endpoint
│       │   ├── auth.py                   # Authentication handler
│       │   └── runner.py                 # App bootstrap & middleware
│       └── __main__.py                   # Entry point
├── pyproject.toml                        # Project metadata & dependencies
├── docker-compose.yml                    # Docker Compose setup
├── Dockerfile                            # Multi-stage Docker build
├── Justfile                              # Task runner
├── ruff.toml                             # Linter configuration
└── ty.toml                               # Type checker configuration
```

---

<a id="api-endpoints"></a>
## 🎯 API Endpoints

### Base URL: `http://127.0.0.1:8082/api/v1`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/crime/add` | No | Create a new crime record |
| `GET` | `/crimes/get?skip=0&limit=100` | No | List crimes (paginated) |
| `GET` | `/crime/:crime_id` | Bearer | Get crime by ID |
| `PUT` | `/crime/update/:crime_id` | No | Update crime by ID |
| `DELETE` | `/crime/:crime_id` | No | Delete crime by ID |

### Health Check: `http://127.0.0.1:8082/health`

### Request/Response Examples

**Create Crime:**
```json
POST /api/v1/crime/add
{
    "type": "Robbery",
    "description": "Bank robbery at Main Street",
    "location": "Downtown",
    "suspect_name": "John Doe",
    "date_time": "2026-05-14T12:00:00",
    "latitude": 40.7128,
    "longitude": -74.0060
}
```

**Response:**
```json
{
    "id": 1,
    "type": "Robbery",
    "description": "Bank robbery at Main Street",
    "location": "Downtown",
    "suspect_name": "John Doe",
    "date_time": "2026-05-14T12:00:00",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "created_at": "2026-05-14T12:00:00+00:00",
    "updated_at": null
}
```

**Error Response (500):**
```json
{
    "status_code": 500,
    "description": "Internal server error",
    "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

---

<a id="architecture"></a>
## 🏗 Architecture

### Layer Diagram

```
┌─────────────────────────────────────┐
│         robyn/ (Web Layer)          │
│    endpoints/ auth/ runner.py       │
├─────────────────────────────────────┤
│      database/ (Data Layer)         │
│  crime_repository.py db_manager.py  │
├─────────────────────────────────────┤
│       domain/ (Domain Layer)        │
│            entities.py              │
├─────────────────────────────────────┤
│    config/ di/ adapters/ logger/    │
│  (Infrastructure & Cross-cutting)   │
└─────────────────────────────────────┘
```

### Key Design Decisions

1. **Pure Repository Functions**: Database operations are async functions, not class methods. Session is passed explicitly — no hidden state, easy to test.
2. **Lazy DI Proxy**: The `Ioc` container uses a proxy pattern with `LazyProvider` to avoid circular imports and enable lazy resolution.
3. **ContextVar-based Request Tracing**: `request_id` is stored in `contextvars.ContextVar` and propagated to middleware, exception handlers, and error responses without passing through function signatures.
4. **Adapter Pattern**: `LoggerConfigAdapter` transforms `AppConfig` into a `LoggerConfig` dataclass — keeps logger module independent of config structure.
5. **SQLite WAL Mode**: Write-Ahead Logging enables concurrent reads without blocking, with performance PRAGMAs tuned for API workloads.

---

<a id="logging-system"></a>
## 📝 Logging System

A sophisticated, production-ready logging system built with `structlog`.

### Features

- **Structured Logging**: All logs are structured events with automatic context injection (filename, function, line number, thread, process).
- **Dual Output**:
  - Development: Colored console output with padded event names.
  - Production: JSON format with `orjson` serialization for log aggregation.
- **Request Tracing**: Every request gets a UUID `request_id` that appears in all related logs and error responses.
- **Middleware Logging**: Request body, headers, IP, and identity are logged at DEBUG level; duration is tracked in nanoseconds.
- **File Rotation**: Configurable log rotation with size limits and backup count.
- **Third-party Hijacking**: Automatically configures log levels for SQLAlchemy, Robyn, Pydantic, aiosqlite, and more.

### Log Output Examples

**Console (Development):**
```
2026-05-14 12:00:00 [info     ] request_id=a1b2c3d4... runner.py:45
2026-05-14 12:00:01 [info     ] request_id=a1b2c3d4... request_path=/api/v1/crime/1 response_duration_ns=1234567 runner.py:58
```

**JSON (Production):**
```json
{"event": "request_id=a1b2c3d4...", "logger": "robyn_example.robyn.runner", "level": "info", "timestamp": "2026-05-14T12:00:00", "filename": "runner.py", "lineno": 45}
```

---

<a id="configuration"></a>
## ⚙️ Configuration

### Environment Variables

All settings can be overridden via environment variables with `__` as nested delimiter:

```bash
ENV_FILE_NAME=".env.prod"
APP__TITLE="Crime API Production"
APP__HOST="0.0.0.0"
APP__PORT=8080
DB__DB_DIR="/data/database"
DB__ECHO=false
LOG__LOG_LEVEL=20
LOG__ENABLE_FILE_LOGGING=true
```

### Default Settings

```python
# Application
app.title = "Robyn Example"
app.host = "127.0.0.1"
app.port = 8082
app.client_timeout_sec = 30
app.keep_alive_timeout_sec = 20

# Database
db.db_schema = "sqlite+aiosqlite"
db.db_dir = "./local_database"
db.db_name = "database.db"
db.pool_size = 3

# Logging
log.log_level = 10  # 10 means "DEBUG", 20 means "INFO", etc
log.console_colors = True
log.enable_file_logging = True

# File System
filesys.logs_dir = "./logs"
filesys.max_log_file_size_mb = 10
filesys.log_backup_count = 5
```

---

<a id="development"></a>
## 🛠 Development

### Setup

```bash
# Install with dev dependencies
uv sync --group dev

# Run linter & formatter
just lint
```

### Code Quality

- **Ruff**: All rules enabled (`select = ["ALL", "ANN", "I"]`), line length 79, Google-style docstrings.
- **ty**: Strict type checking with `all = "error"`.

### Docker

```bash
# Build and run
docker-compose up --build

# Rebuild
docker-compose down && docker-compose build && docker-compose up

# Using Just
just build
```

The Docker image uses a multi-stage build with `uv` for fast dependency installation and runs as a non-root user.

---

<a id="license"></a>
## 📝 License

MIT License – free to use and modify.

---

<div align="center">
  <sub>Built with ❤️ using Robyn, SQLAlchemy, structlog, that-depends and pydantic</sub>
</div>
