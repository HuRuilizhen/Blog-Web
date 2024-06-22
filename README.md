# Blogs

constructed by zhenji (HuRuilizhen)

powered by django, bootstrap3, ckeditor, martor

---

## Package Needed:

run following commands in the terminal

```
    pip install django==4.1.1
    pip install django-bootstrap3==23.1
    pip install django-ckeditor==6.5.1
    pip install django-crispy-form==2.0
    pip install django-js-asset==2.1.0
    pip install martor==1.6.28
    pip install celery==5.4.0
    pip install redis==5.0.3
```

## To make migrations:

run following commands in the terminal

```
    python manage.py makemigrations contents
    python manage.py makemigrations users 
    python manage.py migrate
    python manage.py makemigrations
```

## To create superuser:

run following commands in the terminal

```
    python manage.py createsuperuser
```

## To change debug mode:

change the following statement in Blog\settings.py

### - Turn off debug mode (current)

```python
    DEBUG = False

    ALLOWED_HOSTS = ["*"]
```

### - Turn on debug mode

```python
    DEBUG = True

    ALLOWED_HOSTS = []
```

## To start server:

### - Start server in debug mode on <font color=pink>local machine</font> (for local testing)

run following commands in the terminal

```
    python manage.py runserver
```

default ip: 127.0.0.1
default port: 8000

open browser at 127.0.0.1:8000

### - Start server on <font color=pink> LAN </font>

turn off debug mode (as default), run following commands
```
    python manage.py runserver 0.0.0.0:8000
```
need to turn off fire wall before starting server

<br>

run in insecure mode (do not recommanded)
```
    python manage.py runserver 0.0.0.0:8000 --insecure
```

### - Start server on <font color=pink> INTERNET </font>

run in background in insecure mode (do not recommanded)

```
    nohup python manage.py runserver 0.0.0.0:8000 --insecure
```


