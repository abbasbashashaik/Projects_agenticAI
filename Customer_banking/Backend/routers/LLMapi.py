from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from typing import Type,Optional

agents_router=APIRouter(prefix="/agent",tags=["Agent"])

class Information(BaseModel):
    query:Optional[str]=None

@agents_router.post("/chat")
def ask_agent(data:Information):
    from agent.agents.banking_agent import ask_llm
    if not data.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty or null.")
    return ask_llm(data.query)