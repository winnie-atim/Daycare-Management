from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_ENGINE')

engine = create_engine(
    DATABASE_URL,
    pool_size=10,  
    max_overflow=20,  
    pool_timeout=30, 
    pool_recycle=1800  
)
Session = sessionmaker(bind=engine)
session = Session()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()