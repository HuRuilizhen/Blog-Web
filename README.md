# Blogs

constructed by zhenji (HuRuilizhen)

powered by django, bootstrap3, ckeditor, martor

---

## Package Needed:

run following commands in the terminal

```
    pip django==4.1.1
    pip django-bootstrap3==23.1
    pip django-ckeditor==6.5.1
    pip django-crispy-form==2.0
    pip django-js-asset==2.1.0
    pip martor==1.6.28
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

## To start server

run following commands in the terminal

```
    python manage.py runserver
```