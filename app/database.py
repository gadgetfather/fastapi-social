from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# # Connect to PostgreSQL database using psycopg2

# try:
#     connection = psycopg2.connect(user="postgres",
#                                   password="12345",
#                                   host="localhost",
#                                   dbname="fastapi",
#                                   cursor_factory=RealDictCursor
#     )
#     cursor = connection.cursor()
#     print("Connected to PostgreSQL")
# except (Exception, psycopg2.Error) as error:
#     print("Error while connecting to PostgreSQL", error)
