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

5. Run the application:

    ```
    poetry run uvicorn main:app --reload
    ```

Your application should now be running at `http://localhost:8000`.

## Testing

To run the tests for the application, navigate to the project directory in the terminal and run the following command:

    poetry run pytest