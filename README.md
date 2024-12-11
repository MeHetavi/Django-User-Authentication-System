# Django-User-Authentication-System

1. Create a virtual environment.
    - python -m venv env

2. Clone the repo in the env.

3. Install all requirements.
    - pip install -r requirements.txt

4. Create a .env file in same folder with manage.py file with variables:
    - EMAIL_HOST_USER = 'email address'
    - EMAIL_HOST_PASSWORD = 'app password'

5. Make db migrations.
    - python manage.py makemigrations
    - python manage.py migrate

6. Run the app.
    - python manage.py runserver