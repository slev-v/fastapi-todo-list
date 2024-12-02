FROM python:3.11.9-slim-bullseye as builder

RUN python -m pip install --upgrade pip && \
  pip install poetry==1.8.2

COPY pyproject.toml poetry.lock ./

RUN poetry export --without-hashes --format=requirements.txt --output=requirements.prod.txt

FROM python:3.11.9-slim-bullseye as dev

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY --from=builder requirements.prod.txt ./

RUN apt update -y && \
  apt install -y python3-dev gcc musl-dev && \
  pip install --upgrade pip && \
  pip install --no-cache-dir -r requirements.prod.txt

COPY ./src /app/src
COPY ./tests /app/tests
COPY alembic.ini /app

EXPOSE 8000
