MAIN = poetry run python src/main.py

request: .venv config.yaml
	$(MAIN) request --prompt "$(PROMPT)"

worker: .venv config.yaml
	$(MAIN) worker

migrate: .venv config.yaml
	$(MAIN) migrate

repl: .venv config.yaml
	$(MAIN) repl

server: .venv config.yaml
	$(MAIN) server

install: .venv
	poetry install

.venv:
	poetry env use $(shell which python3.9)

config.yaml:
	cp config.yaml.example $@
