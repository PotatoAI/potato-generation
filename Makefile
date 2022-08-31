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

ui/src/graphql/schema.schema: config.yaml
	echo $(MAIN) export-graphql-schema
	echo 'disable generation from python, using link directly'

generate: ui/src/graphql/schema.schema
	$(MAKE) -C ui generate

ui-start:
	cd ui && npm run start

install: .venv
	poetry install
	$(MAKE) -C ui npm-i

.venv:
	poetry env use $(shell which python3.9)

config.yaml:
	cp config.yaml.example $@

clean:
	rm -f ui/src/graphql/schema.json
	rm -f ui/src/generated/*.ts
