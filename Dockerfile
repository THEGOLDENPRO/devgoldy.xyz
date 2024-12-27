FROM python:3.11-slim-bookworm

USER root

WORKDIR /app

COPY /app ./app
COPY /static ./static
COPY /templates ./templates
COPY /markdown ./markdown

COPY input.css .
COPY requirements.txt .
COPY static_config.toml .
COPY tailwind.config.js .

RUN apt-get update && apt-get install -y git

RUN pip install -r requirements.txt

EXPOSE 8000
ENV LISTEN_PORT = 8000

CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--proxy-headers"]
