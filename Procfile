web: gunicorn ATS.wsgi --pythonpath app --log-file - 
release: python manage.py migrate
main: python app.py
