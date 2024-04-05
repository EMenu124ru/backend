ifeq ($(shell test -e '.envs' && echo -n yes),yes)
	include .envs/django.env
	include .envs/celery.env
	include .envs/postgres.env
endif

args := $(wordlist 2, 100, $(MAKECMDGOALS))
ifndef args
MESSAGE = "No such command (or you pass two or many targets to ). List of possible commands: make help"
else
MESSAGE = "Done"
endif

HELP_FUN = \
	%help; while(<>){push@{$$help{$$2//'options'}},[$$1,$$3] \
	if/^([\w-_]+)\s*:.*\#\#(?:@(\w+))?\s(.*)$$/}; \
    print"$$_:\n", map"  $$_->[0]".(" "x(20-length($$_->[0])))."$$_->[1]\n",\
    @{$$help{$$_}},"\n" for keys %help; \

# Commands
help: ##@Help Show this help
	@echo -e "Usage: make [target] ...\n"
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)

docker-up-build:  ##@Application Run and build application server
	docker-compose up --build --remove-orphans

docker-up-buildd:  ##@Application Run and build application server in daemon
	docker-compose up -d --build --remove-orphans

docker-up:  ##@Application Run application server
	docker-compose up

docker-upd:  ##@Application Run application server in daemon
	docker-compose up -d

docker-down:  ##@Application Stop application in docker
	docker-compose down --remove-orphans

docker-downv:  ##@Application Stop application in docker and remove volumes
	docker-compose down -v --remove-orphans

docker-django-run:  ##@Application Run django container with command
	docker-compose run --rm django $(args)

fill_sample_data:  ##@Application Run script for create sample data in db
	make docker-django-run "make fill_sample_data"

migrate:  ##@Application Apply migrations
	make docker-django-run "make migrate"

makemigrations:  ##@Application Create migrations
	make docker-django-run "make makemigrations"

createsuperuser:  ##@Application Create superuser
	make docker-django-run "make createsuperuser"

shell:  ##@Application Run django shell
	make docker-django-run "make shell"

open-db:  ##@Database Open database inside docker-image
	docker exec -it postgres psql -d $(POSTGRES_DB) -U $(POSTGRES_USER) -p $(POSTGRES_PORT)

tests:  ##@Testing Test application with pytest
	make docker-django-run "make tests"

tests-fast:  ##@Testing Test application with pytest
	make docker-django-run "make tests-fast"

tests-cov:  ##@Testing Test application with pytest and create coverage report
	make docker-django-run "make tests-cov"

linters:  ##@Linters Run linters
	make docker-django-run "make linters"

docker-login:  ##@Docker Login in GitHub Container Registry
	echo $(PAT) | docker login ghcr.io -u $(USERNAME) --password-stdin

docker-clean:  ##@Docker Remove all unused docker objects
	docker system prune --all -f

docker-cleanv:  ##@Docker Remove all docker objects with volumes
	docker system prune --all --volumes -f

docker-pull-prod:  ##@Docker Pulling containers
	docker-compose -f docker-compose.prod.yml pull

docker-stack-deploy:  ##@Docker Deploy containers in stack in docker swarm
	docker stack deploy --with-registry-auth --resolve-image changed --prune --compose-file docker-compose.prod.yml backend

docker-stack-update:  ##@Docker Deploy containers in stack in docker swarm
	docker service update --with-registry-auth --force --image ghcr.io/emenu124ru/django:latest backend_django
	docker service update --with-registry-auth --force --image ghcr.io/emenu124ru/swagger:latest backend_swagger-ui
	docker service update --with-registry-auth --force --image ghcr.io/emenu124ru/alexandria:latest backend_alexandria
	docker service update --with-registry-auth --force --image ghcr.io/emenu124ru/django:latest backend_daphne
	docker service update --with-registry-auth --force --image ghcr.io/emenu124ru/django:latest backend_celery_worker
	docker service update --with-registry-auth --force --image ghcr.io/emenu124ru/django:latest backend_celery_beat
	docker service update --with-registry-auth --force --image ghcr.io/emenu124ru/django:latest backend_flower
	docker service update --with-registry-auth --force --image ghcr.io/emenu124ru/nginx:latest backend_nginx

docker-stack-deploy-portainer:  ##@Docker Deploy containers in stack in docker swarm
	docker stack deploy --with-registry-auth --resolve-image changed --prune --compose-file portainer-agent-stack.yml portainer

docker-stop:  ##@Docker Stop all docker containers
	@docker rm -f $$(docker ps -aq) || true

%::
	echo $(MESSAGE)
