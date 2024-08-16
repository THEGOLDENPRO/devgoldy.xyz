build: install-deps

PIP = pip

install-deps:
	${PIP} install -r requirements.txt

PYTHON = python

docker-build:
	${PYTHON} scripts/docker_build.py

docker-compose:
	docker compose up

run:
	uvicorn app.main:app --reload --port 8083

test:
	ruff .

clean:
	rm ./web/output.css