# Definition of variables
POETRY := poetry


# Basic commands
install:
	@echo "Installing project dependencies..."
	$(POETRY) install



	@echo "Cloning the repositories..."
	git clone git@github.com:vladislav/wellplan.git
	@echo "Navigating to the project directory..."
	cd wellplan
	@echo "Running project setup..."
	make install
	@echo "Creating .env file..."
	cp .env.example .env


# Command for Alembic
#migrate-create:
#Creating a new Alembic migration...
#$(POETRY) run alembic revision --autogenerate -m "Description of the migration"""


migrate:
	@echo "Running Alembic migrations..."
	$(POETRY) run alembic upgrade head


downgrade:
	@echo "Rolling back Alembic migrations..."
	$(POETRY) run alembic downgrade -1


# Run the application
run:
	@echo "Starting the application..."
	$(POETRY) run uvicorn main:app --reload

# Testing
test:
	@echo "Running tests..."
	$(POETRY) run pytest
