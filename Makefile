run-dev:
	uvicorn main:app --port 8000 --log-level debug --reload


COMPOSE_FILE = docker-compose.yml

COMMAND = docker-compose -f ${COMPOSE_FILE} run --rm minimal-fastapi-app /bin/sh -c

build:
	docker-compose -f ${COMPOSE_FILE} build

run:
	docker-compose -f ${COMPOSE_FILE} up

stats:
	docker stats --no-stream

stop-all:
	docker stop $$(docker ps -a -q)

clean:
	@echo "Cleaning up all images ..."
	docker system prune -f --all
	@echo "Cleaning up all volumes ..."
	docker volume prune -f --all

log:
	docker-compose -f ${COMPOSE_FILE} logs minimal-fastapi-app

black-format:
	$(COMMAND) "black --check --diff ."
