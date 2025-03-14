from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base

# SQLite database URL
DATABASE_URL = "sqlite:///./data/db_insurance.db"

# Engine creation
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Session local
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creating the tables
Base.metadata.create_all(bind=engine)

# Dependency: Getting DB session
def get_db():
    """
    Gets the database session
    """
    db = session_local()

    try:
        yield db
    finally:
        db.close()
