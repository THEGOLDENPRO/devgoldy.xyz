build: install-deps

PIP = pip

install-deps:
	${PIP} install -r requirements.txt

PYTHON = python

docker-build:
	${PYTHON} scripts/docker_build.py

docker-compose:
	docker compose up

test:
	ruff check .

clean:
	rm ./web/output.css