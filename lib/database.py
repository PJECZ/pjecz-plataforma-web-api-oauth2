"""
Database
"""
from fastapi import Depends

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config.settings import Settings, get_settings

Base = declarative_base()


def get_db(settings: Settings = Depends(get_settings)):
    """Database dependency"""

    # Create engine
    engine = create_engine(f"postgresql+psycopg2://{settings.db_user}:{settings.db_pass}@{settings.db_host}/{settings.db_name}")

    # Create session
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    try:
        db = session_local()
        yield db
    finally:
        db.close()
