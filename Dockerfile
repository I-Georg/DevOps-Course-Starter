FROM python:3.6.9-slim-buster as base

ARG FLASK_ENV

ENV FLASK_ENV=${FLASK_ENV} \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.6


RUN pip install "poetry==$POETRY_VERSION"

#production
FROM base as production
# Copy only requirements to cache them in docker layer
WORKDIR /todo_app
COPY poetry.lock pyproject.toml .
RUN poetry config virtualenvs.create false --local && poetry install --no-dev --no-root
RUN poetry add gunicorn


# Creating folders, and files for a project:
COPY . /todo_app

EXPOSE 5001
ENTRYPOINT ["./gunicorn.sh"]

#development
FROM base as development
WORKDIR /todo_app
COPY poetry.lock pyproject.toml .
RUN poetry config virtualenvs.create false --local && poetry install --no-dev --no-root


# Creating folders, and files for a project:
COPY . /todo_app
ENV FLASK_ENV='development'
ENV FLASK_APP='todo_app'

EXPOSE 5001

ENTRYPOINT ["poetry", "run","flask", "run", "--host", "0.0.0.0"]
