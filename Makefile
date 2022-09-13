MAIN = poetry run python src/main.py

request: config.yaml
	$(MAIN) request --prompt "$(PROMPT)"

BSRGAN:
	git clone git@github.com:PotatoAI/BSRGAN.git BSRGAN

worker-upscale: config.yaml BSRGAN
	$(MAIN) worker --task-kind upscale

worker-diffusion: config.yaml
	$(MAIN) worker --task-kind diffusion

worker-until-done: config.yaml
	$(MAIN) worker --until-done --task-kind diffusion

migrate: config.yaml
	$(MAIN) migrate

repl: config.yaml
	$(MAIN) repl

server: config.yaml
	$(MAIN) server

wip: config.yaml
	$(MAIN) wip

ui/src/graphql/schema.schema: config.yaml
	echo $(MAIN) export-graphql-schema
	echo 'disable generation from python, using link directly'

generate: ui/src/graphql/schema.schema
	$(MAKE) -C ui generate

ui-start:
	cd ui && npm run start

install:
	poetry install
	$(MAKE) -C ui npm-i

.venv:
	poetry env use $(shell which python3.9)

config.yaml:
	cp config.yaml.example $@

clean:
	rm -f ui/src/graphql/schema.json
	rm -f ui/src/generated/*.ts
