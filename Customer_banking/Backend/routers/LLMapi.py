from fastapi import APIRouter,HTTPException,Depends
from pydantic import BaseModel
from typing import Type,Optional
from sqlalchemy.orm import Session
from db.connection import get_db
from routers.auth import get_current_user
from models.user import User

agents_router=APIRouter(prefix="/agent",tags=["Agent"])

class Information(BaseModel):
    query:Optional[str]=None

@agents_router.post("/chat")
def ask_agent(data:Information,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    from agent.agents.banking_agent import ask_llm
    if not data.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty or null.")
    return ask_llm(data.query,db=db,authenticated_user_id=current_user.id)


