"""
Database
"""
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Configuration load
if Path("instance/settings.py").exists():
    from instance.settings import SQLALCHEMY_DATABASE_URI
else:
    from config.settings import SQLALCHEMY_DATABASE_URI


# SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# SQLAlchemy Base for models
Base = declarative_base()


# SQLAlchemy database session
def get_db():
    """Dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
