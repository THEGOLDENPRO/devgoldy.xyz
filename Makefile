build: install-deps npm-install tailwind

install-deps:
	pip install -r requirements.txt

npm-install:
	npm i

compile-ts:
	tsc ./src/script.ts

tailwind:
	npx tailwindcss -i ./src/input.css -o ./src/output.css

tailwind-watch:
	npx tailwindcss -i ./src/input.css -o ./src/output.css --watch

docker-build:
	python scripts/docker_build.py

docker-compose:
	docker compose up

run:
	uvicorn main:app --reload --port 8083

clean:
	rm ./src/output.css
	rm ./src/script.js