# Project Management Tool

A simple project management tool built with Django.

## Setup Instructions

1. Clone the repository:
    ```bash
    git clone https://github.com/Al-Amin-Raha/project-management-tool.git
    cd src
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Apply the migrations:
    ```bash
    python manage.py migrate
    ```

5. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:
    ```bash
    python manage.py runserver
    ```

7. Open your browser and go to `http://127.0.0.1:8000/` to see the application.

## Requirements

- Python 3.x
- Django 3.x
- Other dependencies listed in `requirements.txt`

