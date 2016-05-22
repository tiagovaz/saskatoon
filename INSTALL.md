# Documentation d'installation

 1 - Installation des packages requis

```
pip install -r requirements.txt
```

 2 - Synchronisation de la base de données

```
python manage.py migrate
```

 3 - Création d'un profil root

```
python manage.py createsuperuser
```

 4 - Lancement du projet

```
python manage.py runserver
```

