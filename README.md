<div align="center">

  # 🌇 [``devgoldy.xyz``](https://devgoldy.xyz/)

  <sub>My main website.</sub>

  <img width="1000px" src="https://github.com/THEGOLDENPRO/devgoldy.xyz/assets/66202304/cf1a7dbb-5598-4de6-8e46-224523aad3f2">

</div>

## Prerequisites
- ~~[NodeJS](https://nodejs.org/en)~~ (no longer needed)
- ~~[Python 3.8+](https://www.python.org/)~~ (Might still work on 3.8 but versions below 3.9 are now depreacted)
- [Python 3.9+](https://www.python.org/)
- [Make](https://www.gnu.org/software/make/) (Optional)

## Run Locally
> [!WARNING]
> As I don't really expect people to run my website other than myself, these instructions will not be maintained hence it can be out of date and not work.

1. Git clone repo.
```sh
git clone https://github.com/THEGOLDENPRO/devgoldy.xyz
```

2. Create python virtual environment.
```sh
cd devgoldy.xyz && python -m venv env
```

3. Activate that environment.
```sh
source env/bin/activate
```
Windows:
```sh
cd env/Scripts && activate
```

4. Install dependencies.
```sh
pip install -r requirements.txt
```

5. Create configuration file.
```sh
cp config.template.toml config.toml
```

6. RUN!!!!
```sh
fastapi dev
```
