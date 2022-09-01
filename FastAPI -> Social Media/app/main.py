from fastapi import FastAPI, HTTPException, status, Response, Depends
from fastapi.params import Body
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import user, post, auth





models.Base.metadata.create_all(bind=engine)

app = FastAPI()     #making a Fastapi object --> app

app.include_router(post.router)
app.include_router(user.router) 
app.include_router(auth.router)

