from sqlalchemy.orm import  sessionmaker
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
load_dotenv()
url = os.getenv("db_url") 
SQL_DATABASE_URL = url
engine = create_engine( SQL_DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False , autocommit = False , bind= engine)
Base = declarative_base()
