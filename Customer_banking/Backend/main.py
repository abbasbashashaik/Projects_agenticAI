from db.connection import Base,engine
from models.Accounts import Account
from models.customers import Customer
from models.cards import Card
from models.transaction import Transaction
from models.user import User

from fastapi import FastAPI
from pydantic import BaseModel,EmailStr
from db.connection import get_db,Session
from datetime import datetime
from fastapi import Depends, FastAPI, HTTPException, status
from routers.auth import router
from routers.LLMapi import agents_router

app = FastAPI(title="Banking")
app.include_router(router)
app.include_router(agents_router)
app.get("/")
def root():
  return {"message":"backend is running successfully"}

