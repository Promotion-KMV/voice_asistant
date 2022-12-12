THIS_FILE := $(lastword $(MAKEFILE_LIST))

help:
	make -pRrq  -f $(THIS_FILE) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

start:
	docker-compose --env-file .env-example up --build $(c)

insert-data:
	docker exec -it etl_postgres bash -c "psql -U app movies_database < db_rus.dump" && docker start etl