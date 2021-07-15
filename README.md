# pjecz-plataforma-web-api-oauth2

API de Plataforma Web con autentificación OAuth2

## Configurar

Genere el `SECRET_KEY` con este comando

    openssl rand -hex 32

Cree un archivo para las variables de entorno `.env`

    # MariaDB en Minos
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

Para Bash Shell cree un archivo `.bashrc` con este contenido

    #!/bin/bash
    if [ -f ~/.bashrc ]; then
            . ~/.bashrc
    fi

    figlet Plataforma Web API OAuth2

    . venv/bin/activate
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

    echo "-- FastAPI"
    echo "   python main.py"
    echo

Cree el archivo instance/settings.py para que cargue las variables de entorno

    """
    Configuración para desarrollo
    """
    from config.settings import DB_NAME, DB_USER, DB_PASS, DB_HOST


    # MariaDB
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

    # PostgreSQL
    # SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

    # SQLite en Minos
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///pjecz_plataforma_web.sqlite3'
