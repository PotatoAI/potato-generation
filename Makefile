MAIN = poetry run python src/main.py

request: config.yaml
	$(MAIN) request --prompt "$(PROMPT)"

worker: config.yaml
	$(MAIN) worker

migrate: config.yaml
	$(MAIN) migrate

repl: config.yaml
	$(MAIN) repl

server: .venv config.yaml
	$(MAIN) server

ui/graphql/schema.json: config.yaml
	$(MAIN) export-graphql-schema

generate: ui/graphql/schema.json
	$(MAKE) -C ui generate

ui-start:
	cd ui && npm run start

install: .venv
	poetry install

.venv:
	poetry env use $(shell which python3.9)

config.yaml:
	cp config.yaml.example $@
