build: install-deps npm-install compile-ts tailwind

pip = pip

install-deps:
	${pip} install -r requirements.txt

npm-install:
	npm i

compile-ts:
	npx tsc ./web/scripts/*.ts --target ES2016

tailwind:
	npx tailwindcss -i ./web/input.css -o ./web/output.css

tailwind-watch:
	npx tailwindcss -i ./web/input.css -o ./web/output.css --watch

python = python

docker-build:
	${python} scripts/docker_build.py

docker-compose:
	docker compose up

run:
	uvicorn app.main:app --reload --port 8083

test:
	ruff .

clean:
	rm ./web/output.css