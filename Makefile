.PHONY: start test

PARALLEL := parallel --tag --lb
PYTHON3 ?= python3
ENV ?= . $(shell pwd)/env/bin/activate; \
    PYTHONPATH=$(shell pwd)


env: requirements.txt
	$(PYTHON3) -m venv env
	for requirement in $^; do \
		$(ENV) $(PYTHON3) -m pip install -r $$requirement; \
	done
	touch $@  # update timestamp


start: env
	$(ENV) make start -C server

test: env
	$(ENV) python3 -i test.py
