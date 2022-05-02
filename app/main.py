from multiprocessing import synchronize
from random import random
from types import new_class
from typing import List, Optional
from fastapi import Response, FastAPI, status, HTTPException, Depends
from fastapi.params import Body

from app import utils
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from app.routers import post, user, auth

from . import models
from .database import engine, get_db
from .schemas import PostCreate, Post, UserCreate, UserResponse


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi',
                                user='postgres', password='password', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("success")
        break
    except Exception as e:
        print("fail", e)
        time.sleep(1)


