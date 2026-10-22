# schemas.py

from typing import List, Literal
from pydantic import BaseModel, Field


class Skill(BaseModel):
    name: str

    status: Literal[
        "matched",
        "partial",
        "missing"
    ]

    score: int = Field(
        ge=0,
        le=100
    )

    evidence: str


class Experience(BaseModel):
    score: int = Field(
        ge=0,
        le=100
    )

    evidence: str


class Recommendation(BaseModel):
    recommendation: str
    reason: str

    priority: Literal[
        "high",
        "medium",
        "low"
    ]


class ResumeEvaluation(BaseModel):

    candidate_summary: str

    skills: List[Skill]

    experience: Experience

    important_missing_skills: List[str]

    strengths: List[str]

    weaknesses: List[str]

    overall_skillMatch_score:float

    recommendations: List[Recommendation]