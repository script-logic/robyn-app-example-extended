FROM python:3.14-slim AS builder

ARG UV_VERSION=0.11.1
ARG USER_ID=1000
ARG USER_NAME=appuser
ARG DIR_RIGHTS=750
ARG WORKDIR=/src

ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        build-essential \
        curl \
        && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid ${USER_ID} ${USER_NAME} && \
    useradd --uid ${USER_ID} --gid ${USER_NAME} --shell /bin/bash --create-home ${USER_NAME}

RUN mkdir -p ${WORKDIR} && \
    chown ${USER_NAME}:${USER_NAME} ${WORKDIR} && \
    chmod ${DIR_RIGHTS} ${WORKDIR}

WORKDIR ${WORKDIR}

RUN pip install --no-cache-dir -i https://pypi.org/simple/ uv==${UV_VERSION}

COPY --chown=${USER_NAME}:${USER_NAME} pyproject.toml uv.lock* ./

RUN uv sync --frozen --no-install-project

FROM python:3.14-slim

ARG USER_ID=1000
ARG DIR_RIGHTS=750
ARG USER_NAME=appuser
ARG WORKDIR=/src
ARG PROJECTDIR_LOCAL=/src
ARG PROJECTDIR_DOCKER=${PROJECTDIR_LOCAL}
ARG VENV_PATH=${WORKDIR}/.venv

RUN groupadd --gid ${USER_ID} ${USER_NAME} && \
    useradd --uid ${USER_ID} --gid ${USER_NAME} --shell /bin/bash --create-home ${USER_NAME}

RUN mkdir -p ${WORKDIR} \
    && chown ${USER_NAME}:${USER_NAME} ${WORKDIR} \
    && chmod ${DIR_RIGHTS} ${WORKDIR}

WORKDIR ${WORKDIR}

COPY --from=builder --chown=${USER_NAME}:${USER_NAME} /src/.venv ${VENV_PATH}

COPY --chown=${USER_NAME}:${USER_NAME} .${PROJECTDIR_LOCAL} ${WORKDIR}${PROJECTDIR_DOCKER}

USER ${USER_NAME}


USER ${USER_NAME}

ENV PYTHONPATH="${WORKDIR}${PROJECTDIR_DOCKER}" \
    PATH="${VENV_PATH}/bin:$PATH"
