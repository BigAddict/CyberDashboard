# app/main.py

from fastapi import FastAPI, Depends
from routers import online, cpus
from sqlmodel import SQLModel
from database import engine

app = FastAPI()
SQLModel.metadata.create_all(engine)

app.include_router(online.router)
app.include_router(cpus.router, prefix="/api")