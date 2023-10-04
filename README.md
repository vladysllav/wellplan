# WellPlan: Healthcare Appointment Management System

WellPlan is a Healthcare Appointment Management System designed to streamline the process of booking, rescheduling, and managing appointments with healthcare providers. This platform aims to modernize the patient experience while also simplifying administrative tasks for medical offices.

## Installation and Usage

Here's how to get the project up and running on your local machine for development and testing.

### Prerequisites

- Python 3.11
- Poetry (Python dependency management tool)
- PostgreSQL

### Setup

1. Clone this repository:

    ```
    git clone git@github.com:vladysllav/wellplan.git
    ```

2. Navigate to the project directory:

    ```
    cd wellplan
    ```

3. Install the project dependencies:

    ```
    poetry install
    ```

4. Create `.env` file and fill out with values from `.env.example`
5. Add linters
    ```
    poetry update
    ```
    ```
    poetry install flake8
    ```
    ```
    poetry install black
    ```
    ```
    poetry install isort
    ```

6.  Install precommit hooks
    ```
    poetry update
    ```
    ```
    poetry install pre-commit
    ```
    ```
    pre-commit install
    ```

    Run testing precommit hooks

    ```
    pre-commit run --all-files
    ```
If you are using Windows, you may have an error related to isort.
To fix it, you need to install additional software in the form of Visual C++ Build Tools or
MinGW (Minimalist GNU for Windows) or Windows Software Development Kit (SDK).
So as not to install additional software.
Comment out the block associated with isort in the .pre-commit-config.yaml file
    -   repo: https://github.com/PyCQA/isort
        rev: 5.12.0
        hooks:
        -   id: isort

and use the command before committing
    ```
    isort .
    ```
7. Run the application:

    ```
    poetry run uvicorn main:app --reload
    ```

Your application should now be running at `http://localhost:8000`.

## Testing

To run the tests for the application, navigate to the project directory in the terminal and run the following command:

    poetry run pytest

## Usage with Docker

Here's how to get project up and running in Docker

1. We use the docker-compose build command for building the images for the services in a consistent and reproducible way, making deployment in different environments easier:

    ```
    docker-compose build
    ```

2. After that, you must run next command, It builds the images if they are not located locally and starts the containers:

    ```
    docker-compose up
    ```
