from fastapi import FastAPI

import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import get_db, engine
models.Base.metadata.create_all(bind=engine)
from .routers import post,user,auth

app = FastAPI()

# Dependency


try:
    connection = psycopg2.connect(user="postgres",
                                  password="12345",
                                  host="localhost",
                                  dbname="fastapi",
                                  cursor_factory=RealDictCursor
    )
    cursor = connection.cursor()
    print("Connected to PostgreSQL")
except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)

my_posts = [
    {"title": "Post 1", "content": "This is post 1","id":1},
    {"title": "Post 2", "content": "This is post 2","id":2},
]


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/api")
def root():
    return {"message": "Hello World 123"}

