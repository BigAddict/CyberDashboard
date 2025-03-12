# app/main.py

from fastapi import FastAPI, Depends
from routers import online, cpus, sessions
from sqlmodel import SQLModel
from database import engine

app = FastAPI()
SQLModel.metadata.create_all(engine)

app.include_router(online.router)
app.include_router(cpus.router, prefix="/api")
app.include_router(sessions.router, prefix="/api")