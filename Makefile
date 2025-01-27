install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:
	black *.py

lint:
	pylint --disable=R,C src/*.py

test:
	python -m pytest -vv --cov=src *.py

all: install lint test