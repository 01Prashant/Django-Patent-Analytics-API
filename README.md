# Django-Patent-Analytics-API

## Problem Overview

This project involves developing a backend API that provides analytical insights on a patent dataset. The goal is to assess ability to work with data, design a functional API, and handle basic data queries and summary statistics. Additionally, the application is containerized using Docker-Compose.

### API Design
- Use Django as the backend framework to build the REST API.
- The API should allow users to:
    - Retrieve basic summary statistics of the dataset (`/summary`).
    - Query the dataset based on one or two parameters (e.g., `/query`).
- Implement at least two endpoints:
    - `/summary`: Returns summary statistics (mean, median, etc.) for numerical columns.
    - `/query`: Filters data based on provided query parameters (e.g., patent year, assignee).

### Docker-Compose
- Containerize the Django application using Docker.
- Use Docker-Compose to manage the services:
- A web service (Django API).

## Requirements
- Django for building the API.
- Pandas and NumPy for data processing and analysis.
- Version control with Git and hosting on GitHub.
- Dockerfile for the Django project.
- `docker-compose.yml` to manage the services.

## Setup and Running the Project

### Prerequisites
- Docker and Docker-Compose installed on your machine.
- Git installed on your machine.

### Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/01Prashant/Django-Patent-Analytics-API-using-Docker.git
    cd Django-Patent-Analytics-API-using-Docker
## 1. Running the API Locally
1. **Set Up a Virtual Environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
2. **Install Dependencies:**

    ```sh
    pip install -r requirements.txt
3. **Run Migrations:**

    ```sh
    python manage.py makemigrations
    python manage.py migrate
4. **Run the Development Server:**

    ```sh
    python manage.py runserver
The API will be accessible at http://127.0.0.1:8000/.
## 1. Running the API with  Docker-Compose

1. **Build and run the Docker containers:**

    ```sh
    docker-compose build
    docker-compose up

2. **Run migrations:**

    ```sh
    docker-compose exec web python manage.py makemigrations
    docker-compose exec web python manage.py migrate
    
3. **Run the data cleaning script:**

    ```sh
    docker-compose exec web python scripts/dataclean.py

4. **API Endpoints:**
    - /summary: Returns summary statistics for numerical columns.
    - /query: Filters data based on query parameters (e.g., patent year, assignee).

## Test these api on postman:

1. No Filters (Return All Query)
- URL: http://localhost:8000/query/
- Method: GET
- Params: None
2. Filter by Assignee
- URL: http://localhost:8000/query/
- Method: GET
- Params:
    - assignee: John Doe
3. Filter by Inventor
- URL: http://localhost:8000/query/
- Method: GET
- Params:
    - inventor: Jane Smith
4. Filter by Filing Date Range
- URL: http://localhost:8000/query/
- Method: GET
- Params:
    - filing_date_start: 2023-01-01
    - filing_date_end: 2023-12-31
5. Filter by Publication Date Range
- URL: http://localhost:8000/query/
- Method: GET
- Params:
    - publication_date_start: 2022-01-01
    - publication_date_end: 2022-12-31
6. Combine Filters
- URL: http://localhost:8000/query/
- Method: GET
- Params:
    - assignee: John Doe
    - inventor: Jane Smith
    - filing_date_start: 2023-01-01
    - filing_date_end: 2023-12-31
    - publication_date_start: 2022-01-01
    - publication_date_end: 2022-12-31
7. For summary 
- URL: http://localhost:8000/summary/
- Method: GET

## Contributing
- Feel free to fork the repository and submit pull requests. Ensure that you follow the coding guidelines and include appropriate tests.
