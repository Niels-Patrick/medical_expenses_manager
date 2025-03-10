from models.region import Region
from models.smoker import Smoker
from models.sex import Sex
from models.patient import Patient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database URL
DATABASE_URL = "sqlite:///./data/db_insurance.db"

# Engine creation
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Session local
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Creating the tables
Base.metadata.create_all(bind=engine)
