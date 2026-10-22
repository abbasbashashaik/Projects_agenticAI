from fastapi import APIRouter
from pydantic import BaseModel
from typing import Type,Optional
from app.agent import ask_llm

agents_router=APIRouter(prefix="/agent",tags=["Agent"])

class Information(BaseModel):
    job_description:str
    resume_txt:str

@agents_router.post("/chat")
def ask_agent(info:Information):
    return ask_llm(info.job_description,info.resume_txt)