ifeq (${PYTHON}, )
override PYTHON=3.6
endif

DOCKER=docker run --rm -it ${EXTRA_DOCKER_OPTS} -v ${PWD}:/ntc-rosetta-conf ntc-rosetta-conf-${PYTHON}:latest

.PHONY: start-dev-containers
start-dev-containers:
	docker-compose build --build-arg PYTHON=$(PYTHON)
	docker-compose up -d

.PHONY: stop-dev-containers
stop-dev-containers:
	docker-compose down

.PHONY: build_test_container
build_test_container:
	docker build \
		--tag ntc-rosetta-conf-${PYTHON}:latest \
		--build-arg PYTHON=${PYTHON} \
		-f Dockerfile .

.PHONY: build_test_containers
build_test_containers:
	make build_test_container PYTHON=3.6

.PHONY: enter-container
enter-container:
	${DOCKER} \
		bash

.PHONY: pytest
pytest:
	${DOCKER} \
		pytest --cov=ntc_rosetta_conf --cov-report=term-missing -vs ${ARGS}

.PHONY: black
black:
	${DOCKER} \
		black --check .

.PHONY: sphinx-test
sphinx-test:
	${DOCKER} \
		sphinx-build -W -n -E -q -N -b dummy -d docs/_build/doctrees docs /tmp/asd

.PHONY: pylama
pylama:
	${DOCKER} \
		pylama .

.PHONY: mypy
mypy:
	${DOCKER} \
		mypy .

.PHONY: nbval
nbval:
	docker-compose exec jupyter pytest -vvvvvs --nbval docs/tutorials

.PHONY: _docs
_docs:
	cd docs && make html

.PHONY: docs
docs:
	${DOCKER} \
		make _docs

.PHONY: _jupyter
_jupyter:
	${DOCKER} jupyter notebook --allow-root --ip=0.0.0.0 --NotebookApp.token=''

.PHONY: jupyter
jupyter:
	make _jupyter EXTRA_DOCKER_OPTS="-p 8888:8888"

.PHONY: tests
tests: build_test_containers black pylama mypy start-dev-containers nbval
	make stop-dev-containers

.PHONY: publish
publish:
	${DOCKER} \
		poetry publish --build --username=$(PYPI_USER) --password="$(PYPI_PASSWORD)"
