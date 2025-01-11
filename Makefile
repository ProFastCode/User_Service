DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env
API_FILE = docker_compose/api.yaml
API_CONTAINER = api

.PHONY: api
api:
	${DC} -f ${API_FILE} ${ENV} up --build -d

.PHONY: app-down
api-down:
	${DC} -f ${API_FILE} down

.PHONY: api-shell
api-shell:
	${EXEC} ${API_CONTAINER} bash

.PHONY: api-logs
api-logs:
	${LOGS} ${API_CONTAINER} -f

.PHONY: test
test:
	${EXEC} ${API_CONTAINER} pytest
