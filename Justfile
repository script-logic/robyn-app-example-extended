# Windows: use Git Bash

dc_file := "docker-compose.yml"
dc := "docker-compose -f " + dc_file
TIMEOUT := "timeout /t 5 /nobreak > nul"
PYTEST := "poetry run pytest"
DOCKER_PROD := "docker-compose -f docker-compose.prod.yml"
DOCKER_DEV := "docker-compose -f docker-compose.dev.yml"
DOCKER_TEST := "docker-compose -f docker-compose.test.yml"

os := env_var_or_default("OS", "Linux")

export ENV_FILE_NAME := ".env.test"

default:
    @just --list

run:
    uv run python -m src

build-prod:
    {{DOCKER_PROD}} up -d --build

rebuild-prod:
    {{DOCKER_PROD}} down && {{DOCKER_PROD}} build && {{DOCKER_PROD}} up -d

build-dev:
    {{DOCKER_DEV}} up -d --build

rebuild-dev:
    {{DOCKER_DEV}} down && {{DOCKER_DEV}} build && {{DOCKER_DEV}} up -d

test-unit:
    {{PYTEST}} tests/unit -v

test-integration:
    @just test-up
    {{TIMEOUT}}
    {{PYTEST}} tests/integration -v -m "not slow"
    @just test-down

test-stress:
    @just test-up
    {{TIMEOUT}}
    {{PYTEST}} tests/integration/test_stress.py -v -s
    @just test-down

test-all:
    @just test-unit
    @just test-up
    {{TIMEOUT}}
    {{PYTEST}} tests/ -v -m "not slow"
    @just test-stress
    @just test-down

test-up:
    {{DOCKER_TEST}} down -v
    {{DOCKER_TEST}} build
    {{DOCKER_TEST}} up -d

test-down:
    {{DOCKER_TEST}} down -v

lint:
    @just fix
    @just typecheck

fix:
    uv run ruff format src/
    uv run ruff check src/ --fix

typecheck:
    uv run ty check src/
