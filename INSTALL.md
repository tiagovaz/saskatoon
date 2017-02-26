# Install process

1. Create a virtual environment
    ```
    virtualenv -p python3 ve
    . ve/bin/activate
    ```

2. Installation of python requirements
    ```
    pip3 install -r requirements.txt
    ```

3. Change settings of the DB connexion
    You need to change setting of the DB connexion in function of your installation.
    [Some information here](https://docs.djangoproject.com/en/1.10/ref/databases/)
    ```
       DATABASES = {
           'default': {
               'ENGINE': 'django.db.backends.mysql',
               'NAME': 'saskatoon',
               'USER': 'your_username',
               'PASSWORD': 'your_password',
           }
       }
    ```
    
4. Initialisation of the DB
    ```
    cd saskatoon
    python3 manage.py migrate
    ```

5. Create administrator account
    ```
    python3 manage.py createsuperuser
    ```

# Usage

**To launch the project :**
```
python3 manage.py runserver
```

