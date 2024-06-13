.PHONY: run test reset-migration install

run:
	python app.py

install:
	pip install -r requirements.txt
	${MAKE} run

test:
	FLASK_ENV=testing pytest

reset-migration:
	rm -rf migrations
	flask db init
	flask db migrate -m "Initial migration"
	flask db upgrade
	@echo "Reset migration complete."

update-pkg:
	pip freeze -r requirements.txt

# Default target
.DEFAULT_GOAL := run
