from fastapi import FastAPI
from pydantic import BaseModel,EmailStr
from db.connection import get_db,Session
from datetime import datetime
from fastapi import Depends, FastAPI, HTTPException, status
from models.users import User
from routers.auth import router
from routers.agent_call import agents_router
app = FastAPI(title="ResumeAgent")
app.include_router(router)
app.include_router(agents_router)
app.get("/")
def root():
  return {"message":"backend is running successfully"}


