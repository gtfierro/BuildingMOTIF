# Developer Documentation 

# Installing
Install [Python >= 3.8.0](https://www.python.org/downloads/).
```
pip install buildingmotif
```

# Running on Docker
1. Set config file.
    ```
    cp configs.py.dist configs.py

    echo "DB_URI = 'postgresql://buildingmotif:password@buildingmotif-db'" > configs.py
    ```
2. Up containers with docker-compose.
    ```
    docker-compose up --build
    ```
3. Inside `buildingmotif-api`, migrate db.
    ```
    docker exec -it buildingmotif-api alembic upgrade head
    ```
4. The api can now be reached at http://127.0.0.1:5000 and the app can be reached but http://localhost:4200.

# Using
See the `notebooks` directory. 

# Developing
1. Install [Python >= 3.8.0](https://www.python.org/downloads/).
2. Install [Poetry](https://python-poetry.org/docs/#installation).
3. Clone, download, or fork this repository.
4. Install dependenices with poetry.
    ```
    poetry install
    poetry run pre-commit install
    ```
5. To initialize your database, create your local configs file, enter your db uri, and run the migrations.
    ```
    cp configs.py.dist configs.py

    echo "DB_URI = 'sqlite:////path/to/db.db'" > configs.py

    poetry run alembic upgrade head
    ```
## Uping the API
``` 
poetry run python buildingmotif/api/app.py
```
API will run on localhost:5000

## Testing
``` 
poetry run pytest
```
To run tests with DEBUG prints add the `-o log_cli=true` argument to the command

## Formatting
```
poetry run black .
poetry run isort .
poetry run pylama
```

## Migrating
After making changes to the tables, you must make a new db migration.
```
poetry run alembic revision -m "Description of Changes." --autogenerate
```
Additional changes may need to be made to the migration, so be sure to check it. [Read here](https://alembic.sqlalchemy.org/en/latest/autogenerate.html#auto-generating-migrations) for more information on alembic autogenerate migrations.

## Documenting
Documentation can be built locally with the following command, which will make the HTML files in the `docs/build/html/` directory.

```
cd docs
poetry run make html
```

## Building and Publishing
```
# build and publish test
poetry publish --build --dry-run

# build and publish
poetry publish --build
```

## Web App

1. [Download Node.js](https://nodejs.org/en/download/)
2. [Install Angular](https://angular.io/guide/setup-local)
3. See [buildingmotif-app/README.md](buildingmotif-app/README.md)