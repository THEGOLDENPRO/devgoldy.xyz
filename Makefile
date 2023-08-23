build:
	echo "No build UwU"

run:
	npx tailwindcss -i ./src/input.css -o ./src/output.css --watch

pull-submodules:
	git submodule update --init --recursive

clean:
	rm -r ./build
	rm ./src/output.css
	