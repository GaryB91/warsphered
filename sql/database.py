from sqlite3 import SQLITE_ALTER_TABLE
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@db:5432/warsphered"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # connect_args={}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
