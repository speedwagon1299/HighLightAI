install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:
	black *.py

lint:
	pylint --disable=R,C src/*.py

test:
	python -m pytest -vv --cov=src tests/

all: install lint test