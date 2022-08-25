# pjecz-plataforma-web-api-oauth2

API de Plataforma Web con autentificación OAuth2

## Mejores practicas

Se va a mejorar con los consejos en [I've been abusing HTTP Status Codes in my APIs for years](https://blog.slimjim.xyz/posts/stop-using-http-codes/)

### Escenario exitoso

Status code: **200**

Body

    {
        "result": true,
        "payload": {
            "id": 1,
            "name": "slim",
            "surname": "jim",
            "email:" "james@slimjim.xyz",
            "role": "chief doughnut"
        }
    }

### Escenario fallido: registro no encontrado

Status code: **200**

Body

    {
        "result": false,
        "errorMessage": "No employee found for ID 100"
    }

### Escenario fallido: ruta incorrecta

Status code: **404**

## Configure Poetry

Por defecto, el entorno se guarda en un directorio unico en `~/.cache/pypoetry/virtualenvs`

Modifique para que el entorno se guarde en el mismo directorio que el proyecto

    poetry config --list
    poetry config virtualenvs.in-project true

Verifique que este en True

    poetry config virtualenvs.in-project

## Configurar

Genere el `SECRET_KEY`

    openssl rand -hex 32

Cree un archivo para las variables de entorno `.env`

    # Database
    DB_HOST=127.0.0.1
    DB_NAME=pjecz_plataforma_web
    DB_PASS=****************
    DB_USER=adminpjeczplataformaweb

    # OAuth2
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ALGORITHM=HS256
    SECRET_KEY=****************************************************************

    # Salt sirve para cifrar el ID con HashID, debe ser igual que en la app Flask
    SALT=************************

Cree el archivo `instance/settings.py` que cargue las variables de entorno

    """
    Configuración para desarrollo
    """
    import os

    # Base de datos
    DB_USER = os.environ.get("DB_USER", "wronguser")
    DB_PASS = os.environ.get("DB_PASS", "badpassword")
    DB_NAME = os.environ.get("DB_NAME", "pjecz_plataforma_web")
    DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")

    # PostgreSQL
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

    # CORS or "Cross-Origin Resource Sharing" refers to the situations when a frontend
    # running in a browser has JavaScript code that communicates with a backend,
    # and the backend is in a different "origin" than the frontend.
    # https://fastapi.tiangolo.com/tutorial/cors/
    ORIGINS = [
        "http://localhost:8002",
        "http://localhost:3000",
        "http://127.0.0.1:8002",
        "http://127.0.0.1:3000",
    ]

Para Bash Shell cree un archivo `.bashrc` que se puede usar en el perfil de Konsole

    if [ -f ~/.bashrc ]; then
        source ~/.bashrc
    fi

    source .venv/bin/activate
    if [ -f .env ]; then
        export $(grep -v '^#' .env | xargs)
    fi

    figlet Plataforma Web API OAuth2
    echo

    echo "== Variables de entorno"
    export $(grep -v '^#' .env | xargs)
    echo "   ACCESS_TOKEN_EXPIRE_MINUTES: ${ACCESS_TOKEN_EXPIRE_MINUTES}"
    echo "   DB_HOST: ${DB_HOST}"
    echo "   DB_NAME: ${DB_NAME}"
    echo "   DB_USER: ${DB_USER}"
    echo "   DB_PASS: ${DB_PASS}"
    echo "   SALT: ${SALT}"
    echo "   SECRET_KEY: ${SECRET_KEY}"
    echo

    export PGHOST=$DB_HOST
    export PGPORT=5432
    export PGDATABASE=$DB_NAME
    export PGUSER=$DB_USER
    export PGPASSWORD=$DB_PASS

    alias arrancar="uvicorn --port 8002 --reload plataforma_web.app:app"
    echo "-- FastAPI"
    echo "   arrancar"
    echo

## Instalacion

Clone el repositorio `pjecz-plataforma-web-api-oauth2`

    cd ~/Documents/GitHub/PJECZ
    git clone https://github.com/PJECZ/pjecz-plataforma-web-api-oauth2.git
    cd pjecz-plataforma-web-api-oauth2

Instale el entorno virtual y los paquetes necesarios

    poetry install

## FastAPI

Ejecute el script `arrancar.py` que contiene el comando y parametros para arrancar el servicio

    ./arrancar.py

O use el comando para arrancar con uvicorn

    uvicorn --host=127.0.0.1 --port 8002 --reload plataforma_web.app:app

O use el comando para arrancar con gunicorn

    gunicorn --workers=2 --bind 127.0.0.1:8002 plataforma_web.app:app

## Command Line Interface

Lea `cli/README.md` para saber como configurar el CLI

Ejecute el script `cli/app.py`

    cli/app.py --help

## Google Cloud deployment

Crear el archivo `requirements.txt`

    poetry export -f requirements.txt --output requirements.txt --without-hashes

Y subir a Google Cloud

    gcloud app deploy
