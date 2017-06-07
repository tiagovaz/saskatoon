# Installation guide

Please follow each part of this documentation to install the project.

## Installation of requirements

All requirements are present in the `requirements.txt` file at the project's root.

> You can optionnaly use `virtualenv` to manage your dependencies.
```
cd /.../saskatoon
virtualenv ve
. ve/bin/activate
```

To install requirements use :
```
cd /.../saskatoon
pip install -r requirements.txt
pip install django-leaflet jsonfield
```

## Database migration

We use an `sqlite3` database in our development environment because it's really fast to setup.

> You can optionnaly configure other database engines. Please refer to [this Django documentation](https://docs.djangoproject.com/en/1.11/ref/settings/#databases).

For local instances you can use the base setting file provided as settings-base.py:

```
mv saskatoon/saskatoon/settings-base.py saskatoon/settings.py
```

To migrate the database use :
```
cd /.../saskatoon/saskatoon
python manage.py migrate
```

## Create administrator account

This part is optionnal but you can create a new administrator account to access the admin panel.

This admin panel allow you to see all data of the DB and make some action on it.

To create a new administrator account use :
```
cd /.../saskatoon/saskatoon
python3 manage.py createsuperuser
```

To access the admin panel go on :
```
localhost:8000/admin
```

## Launch the server

Django have an embedded server for development purpose. To run the development server use :

```
cd /.../saskatoon/saskatoon
python manage.py runserver 8000
```
