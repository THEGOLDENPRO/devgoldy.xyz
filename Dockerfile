FROM python:3.13.12-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:0.11.2 /uv /uvx /bin/

USER root

WORKDIR /app

COPY /app ./app
COPY /static ./static
COPY /templates ./templates
COPY /markdown ./markdown

COPY input.css .
COPY pyproject.toml .
COPY static_config.toml .
COPY tailwind.config.js .

RUN apt-get update && apt-get install -y git

COPY uv.lock .
RUN uv sync --locked --no-dev

EXPOSE 8000
ENV LISTEN_PORT=8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host=0.0.0.0", "--proxy-headers"]