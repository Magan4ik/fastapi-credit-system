# fastapi-credit-system

A modern FastAPI-based backend template for a credit management system, using MySQL and Docker.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [About Project](#about-project)

---

## Quick Start

1. **Clone the repository**

    ```sh
    git clone https://github.com/Magan4ik/fastapi-credit-system.git
    cd fastapi-credit-system
    ```

2. **Make sure `wait-for-it.sh` is executable**
3. 
    ```sh
    chmod +x wait-for-it.sh
    ```

    > **Note:** This step is required for the container to run the script properly. If you skip it, you’ll get a `Permission denied` error on startup.

4. **Build and launch the stack**

    ```sh
    docker compose up --build
    ```

5. **Access the application**

    - FastAPI app: [http://localhost:8000](http://localhost:8000)
    - MySQL: [localhost:3306](localhost:3306) — credentials can be found in `docker-compose.yml`

---

## Project Structure

- `docker-compose.yml` — Docker Compose configuration (API and MySQL)
- `wait-for-it.sh` — script to ensure MySQL is ready before the API starts
- `import_db.py` — script for importing initial/sample data
- `alembic/` — database migrations
- `main.py` — FastAPI entrypoint

---

## About Project
A modern asynchronous FastAPI web application for managing banking credits, payments, and credit plans. The project uses asynchronous MySQL connections via SQLAlchemy ORM for data storage.

### Endpoints
`/user_credits/{user_id}` – Retrieve information about a user’s credits
`/plans_performance` – Report on plan performance from the beginning of the month up to the specified day
`/year_performance` – Report on plan performance for the specified year
`/plans_insert` – Add new plans via an Excel file (see example `excel_example.xlsx` in the repository)
`/auth/token` – JWT authentication
`/auth/create_admin` – Create an admin. An authorized admin has access to all the endpoints above.
In this project, User is treated as a client, so Admin is a separate model for authentication.
This endpoint exists only for convenience and should not be present in production.
