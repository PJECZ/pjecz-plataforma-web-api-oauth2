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

## Configurar

Genere el `SECRET_KEY` con este comando

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

    # Comandos Click
    BASE_URL=http://127.0.0.1:8002
    USERNAME=nombre.apellido@pjecz.gob.mx
    PASSWORD=****************


Para Bash Shell cree un archivo `.bashrc` con este contenido

    if [ -f ~/.bashrc ]; then
        source ~/.bashrc
    fi

    source venv/bin/activate
    if [ -f .env ]; then
        export $(grep -v '^#' .env | xargs)
    fi

    figlet Plataforma Web API OAuth2
    echo

    echo "-- Database"
    echo "   DB_HOST: ${DB_HOST}"
    echo "   DB_NAME: ${DB_NAME}"
    echo "   DB_PASS: ${DB_PASS}"
    echo "   DB_USER: ${DB_USER}"
    echo
    echo "-- OAuth2"
    echo "   ACCESS_TOKEN_EXPIRE_MINUTES: ${ACCESS_TOKEN_EXPIRE_MINUTES}"
    echo "   ALGORITHM:                   ${ALGORITHM}"
    echo "   SECRET_KEY:                  ${SECRET_KEY}"
    echo
    echo "-- Jupyter notebooks"
    echo "   PYTHONPATH: ${PYTHONPATH}"
    echo

    export PGDATABASE=${DB_NAME}
    export PGPASSWORD=${DB_PASS}
    export PGUSER=${DB_USER}
    echo "-- PostgreSQL"
    echo "   PGDATABASE: ${PGDATABASE}"
    echo "   PGPASSWORD: ${PGPASSWORD}"
    echo "   PGUSER:     ${PGUSER}"
    echo

    alias arrancar="uvicorn --port 8002 --reload plataforma_web.app:app"
    echo "-- FastAPI"
    echo "   arrancar"
    echo

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

    # MariaDB o MySQL
    # SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

    # PostgreSQL
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

    # SQLite
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///pjecz_plataforma_web.sqlite3'

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

## Crear Entorno Virtual

Crear el enorno virtual dentro de la copia local del repositorio, con

    python -m venv venv

O con virtualenv

    virtualenv -p python3 venv

Active el entorno virtual, en GNU/Linux con...

    source venv/bin/activate

O en Windows con

    venv/Scripts/activate

Verifique que haya el mínimo de paquetes con

    pip list

Actualice el pip de ser necesario

    pip install --upgrade pip

Y luego instale los paquetes requeridos

    pip install -r requirements.txt

Verifique con

    pip list

## FastAPI

Arrancar con uvicorn

    uvicorn --host=0.0.0.0 --port 8002 --reload plataforma_web.app:app

O arrancar con gunicorn

    gunicorn -w 4 -k uvicorn.workers.UvicornWorker plataforma_web.app:app
