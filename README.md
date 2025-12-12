# COM7033 — Assignment (surajyawnumah)

[![CI](https://github.com/CS-LTU/com7033-assignment-surajyawnumah/actions/workflows/ci.yml/badge.svg)](https://github.com/CS-LTU/com7033-assignment-surajyawnumah/actions)
[![Coverage](https://codecov.io/gh/CS-LTU/com7033-assignment-surajyawnumah/branch/main/graph/badge.svg)](https://codecov.io/gh/CS-LTU/com7033-assignment-surajyawnumah)

A small Flask-based application and supporting scripts for the COM7033 assignment. This repository includes the application entrypoint, database initialization and seeding scripts, a CSV dataset used for seeding, and helper/testing scripts.

## Contents

- app.py — Flask application (main entrypoint)
- config.py — Configuration values used by the app
- init_db.py — Initialize the project's database (create schema, tables)
- seed_db.py — Seed the database using seeded_dataset.csv
- seeded_dataset.csv — Dataset used to populate the database
- requirements.txt — Python dependencies
- test.py — Basic tests / example usage
- models/ — ORM and Mongo models
- templates/ — HTML templates for web views
- utils/ — helper modules and utilities

## Features

- Flask web application with user authentication (login/register)
- Database initialization and seeding utilities
- CSV dataset included to reproduce seeded data
- Basic test / example script

## Tech stack

- Python 3.8+ (recommended)
- Flask
- SQLite for relational models (or configured DB in config.py)
- MongoDB used for allergies/assessments models (see models.mongo)
- Dependencies: see requirements.txt

## Quickstart — Setup / Installation

1. Clone the repository:
   ```
   git clone https://github.com/CS-LTU/com7033-assignment-surajyawnumah.git
   cd com7033-assignment-surajyawnumah
   ```

2. Create and activate a virtual environment (recommended):
   - macOS / Linux:
     ```
     python -m venv .venv
     source .venv/bin/activate
     ```
   - Windows (PowerShell):
     ```
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure environment (if needed):
   - Inspect `config.py` to set database URIs, SECRET_KEY, or other variables.
   - For MongoDB-backed functionality, ensure Mongo is reachable and configured in `config.py` or your environment.

## Initialize and Seed the Database

1. Initialize the relational DB schema:
   ```
   python init_db.py
   ```

2. Seed the database with the provided CSV data:
   ```
   python seed_db.py
   ```
   The seeding script reads `seeded_dataset.csv` and inserts records into the database. Confirm the DB configuration in `config.py` before running.

## Run the Application

Run the Flask app locally:
```
python app.py
```
By default the app will run on the host/port configured in `app.py` (commonly http://127.0.0.1:5000). Open a browser at that address to interact with the HTML views.

## Usage — concrete endpoint examples

Below are concrete examples for the endpoints observed in the application entrypoint. Use these examples to exercise the application from the command line with curl. Replace host/port and payload values as appropriate.

- Home page (GET)
  ```
  curl -i http://127.0.0.1:5000/
  ```

- About page (GET)
  ```
  curl -i http://127.0.0.1:5000/about
  ```

- Login (POST)
  - Endpoint: `/login`
  - Form fields: `email`, `password`
  - Example:
    ```
    curl -i -c cookies.txt -X POST http://127.0.0.1:5000/login \
      -d "email=alice@example.com" \
      -d "password=SecretPassword123"
    ```
    Notes:
    - Successful login sets a session cookie. The example stores cookies to `cookies.txt` so you can reuse the session on subsequent requests.
    - On successful login the app redirects to a patient management page (in code it redirects to the route named `patient_managment`).

- Register (POST)
  - Endpoint: `/register`
  - Form fields seen in the app: `first_name`, `last_name`, `email`, `password`, `confirm_password`, `role`
  - Example:
    ```
    curl -i -c cookies.txt -X POST http://127.0.0.1:5000/register \
      -d "first_name=Alice" \
      -d "last_name=Smith" \
      -d "email=alice@example.com" \
      -d "password=SecretPassword123" \
      -d "confirm_password=SecretPassword123" \
      -d "role=doctor"
    ```

- Logout (likely)
  - Many Flask apps include a logout route; if present it will be something like:
    ```
    curl -i -b cookies.txt http://127.0.0.1:5000/logout
    ```
    Check `app.py` for the exact route name.

- Authenticated requests
  - After logging in and storing the cookie (see `-c cookies.txt`), include the cookie for authenticated endpoints:
    ```
    curl -i -b cookies.txt http://127.0.0.1:5000/some-protected-route
    ```

- Patient / Allergy / Assessment functionality
  - The code imports models and helpers for patients, allergies and assessments. Typical routes in this project will include patterns similar to:
    - GET /patients
    - GET /patients/<id>
    - POST /patients (create)
    - GET /patients/<id>/allergies
    - POST /patients/<id>/allergies
    - GET /patients/<id>/assessments
    - POST /patients/<id>/assessments
  - Please confirm exact route names in `app.py` before scripting automated calls.

## Testing / Example script

There is a `test.py` file included for basic smoke-tests / example usage. Run it like:
```
python test.py
```
Adjust the script if your host/port or endpoints differ.

## CI & Coverage badges

- The badges at the top reference a GitHub Actions workflow and Codecov; to make them functional:
  - Add the GitHub Actions workflow file `.github/workflows/ci.yml` (provided alongside this README).
  - Configure Codecov: add codecov upload step in the CI and, if needed, repository token in repository settings.
  - After CI runs and Codecov receives reports, the badges will reflect status.

## Development notes & recommendations

- Keep `config.py` values that are secrets outside of source control. Use environment variables or a `.env` file with python-dotenv.
- If using SQLite locally, add the DB file to `.gitignore`.
- Add a `requirements-dev.txt` for testing/linting tools and a CI workflow that runs tests.
- Consider adding OpenAPI documentation (Swagger) for the API endpoints to make usage explicit.

## Troubleshooting

- Database connection errors: verify `config.py` values for database URIs and ensure the DB server is reachable.
- Dependency issues: recreate the virtual environment and reinstall:
  ```
  rm -rf .venv
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

## License

Add a LICENSE file to the repo (e.g., MIT) and reference it here.

## Author

Suraj Yaw Numah (surajyawnumah)
