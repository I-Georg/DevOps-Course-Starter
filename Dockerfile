FROM python:3.6.13-slim-buster

ARG FLASK_ENV

ENV FLASK_ENV=${FLASK_ENV} \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.6

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /todo_app
COPY poetry.lock pyproject.toml .
RUN poetry config virtualenvs.create false --local && poetry install --no-dev --no-root
RUN poetry add gunicorn


# Creating folders, and files for a project:
COPY . /todo_app
#EXPOSE 5000

ENTRYPOINT ["./gunicorn.sh"]
