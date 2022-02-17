env:
	python -m venv env;

init:
	pip install -r requirements.txt

test:
	python3 ./tests/basic_test.py

.PHONY: env init test
