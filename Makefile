build: install-deps npm-install tailwind

install-deps:
	pip install -r requirements.txt

npm-install:
	npm i

compile-ts:
	tsc ./web/script.ts

tailwind:
	npx tailwindcss -i ./web/input.css -o ./web/output.css

tailwind-watch:
	npx tailwindcss -i ./web/input.css -o ./web/output.css --watch

docker-build:
	python scripts/docker_build.py

docker-compose:
	docker compose up

run:
	uvicorn app.main:app --reload --port 8083

test:
	ruff .

clean:
	rm ./web/output.css
	rm ./web/script.js