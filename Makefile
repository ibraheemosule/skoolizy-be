.PHONY: run test reset-migration install update-pkg

# Default target
.DEFAULT_GOAL := run

# Run the Flask app
run:
	python app.py

# Install dependencies and run the application
install:
	pip install -r requirements.txt
	$(MAKE) run

# Run tests with pytest in testing environment
test:
	FLASK_ENV=testing pytest

# Reset the database migrations
reset-migration:
	rm -rf migrations
	flask db init
	flask db migrate -m "Initial migration"
	flask db upgrade
	@echo "Reset migration complete."

# Update the requirements file with current installed packages
update-pkg:
	pip freeze > requirements.txt

