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

3. Initialisation of the DB
    ```
    cd saskatoon
    python3 manage.py migrate
    ```

4. Create administrator account
    ```
    python3 manage.py createsuperuser
    ```

# Usage

**To launch the project :**
```
python3 manage.py runserver
```

