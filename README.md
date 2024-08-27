# Instructions on how to use it.

create a .env file in website dir
and add these codes

create db and add the info
- DEBUG=True
- SECRET_KEY=""
- DB_DATABASE=
- DB_USER=
- DB_PASSWORD=
- DB_IP="127.0.0.1"
- DB_PORT=5432


1. Download the code.
2. python3 -m venv venv
3. source venv/bin/activate
4. pip install -r requirements.txt
5. python3 manage.py makemigrations
6. python3 manage.py migrate 
7. python3 manage.py runserver
