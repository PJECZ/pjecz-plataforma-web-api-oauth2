# pjecz-plataforma-web-api-oauth2

API de Plataforma Web con autentificación OAuth2

## Configurar

Genere el `SECRET_KEY` con este comando

    openssl rand -hex 32

Cree un archivo para las variables de entorno `.env`

    # Base de datos
    DB_USER=pjeczadmin
    DB_PASS=****************
    DB_NAME=pjecz_plataforma_web
    DB_HOST=127.0.0.1

    # OAuth2
    SECRET_KEY=****************************************************************
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30

    # Jupyter notebooks
    PYTHONPATH=/ruta/al/directorio/GitHub/guivaloz/pjecz-plataforma-web-api-oauth2
    USERNAME=nombres.apellido_paterno@pjecz.gob.mx
    PASSWORD=****************

Para Bash Shell cree un archivo `.bashrc` con este contenido

    #!/bin/bash
    if [ -f ~/.bashrc ]; then
        . ~/.bashrc
    fi

    source venv/bin/activate

    figlet Plataforma Web API OAuth2

    export $(grep -v '^#' .env | xargs)
    echo "-- Variables de entorno"
    echo "   DB_USER: ${DB_USER}"
    echo "   DB_PASS: ${DB_PASS}"
    echo "   DB_NAME: ${DB_NAME}"
    echo "   DB_HOST: ${DB_HOST}"
    echo "   SECRET_KEY: ${SECRET_KEY}"
    echo "   ALGORITHM: ${ALGORITHM}"
    echo "   ACCESS_TOKEN_EXPIRE_MINUTES: ${ACCESS_TOKEN_EXPIRE_MINUTES}"
    echo "   PYTHONPATH: ${PYTHONPATH}"
    echo

    alias arrancar="uvicorn plataforma_web.app:app --port 8002 --reload"
    echo "-- Aliases"
    echo "   arrancar = uvicorn plataforma_web.app:app --port 8002 --reload"
    echo

Cree el archivo `instance/settings.py` que cargue las variables de entorno

    """
    Configuración para desarrollo
    """
    import os


    DB_USER = os.environ.get("DB_USER", "wronguser")
    DB_PASS = os.environ.get("DB_PASS", "badpassword")
    DB_NAME = os.environ.get("DB_NAME", "pjecz_plataforma_web")
    DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")

    # MariaDB o MySQL
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

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

## Jupyter notebooks

Instale el kernel para ejecutar notebooks de Jupyter en VSCode

    pip install ipykernel pandas requests
