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
from starlette.middleware.sessions import SessionMiddleware
import os

app = FastAPI(title="Banking")

app.add_middleware(
    SessionMiddleware,
    secret_key=os.environ["SESSION_SECRET"],
    session_cookie="banking_session",
    same_site="lax",
    https_only=False,  # Set False only for local HTTP development
    max_age=1800,
)

app.include_router(router)
app.include_router(agents_router)
app.get("/")
def root():
  return {"message":"backend is running successfully"}

