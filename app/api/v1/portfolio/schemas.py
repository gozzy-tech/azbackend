import uuid
from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, HttpUrl, field_validator


# ───────────── Project ─────────────

class ProjectBase(BaseModel):
    title: str
    description: str
    tech_stack: List[str]
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    image_url: Optional[str] = None
    category: str
    is_featured: bool = False


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    tech_stack: Optional[List[str]] = None
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    is_featured: Optional[bool] = None


class ProjectResponse(ProjectBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ───────────── Experience ─────────────

class ExperienceBase(BaseModel):
    company: str
    role: str
    description: str
    start_date: date
    end_date: Optional[date] = None
    is_current: bool = False


class ExperienceCreate(ExperienceBase):
    pass


class ExperienceUpdate(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_current: Optional[bool] = None


class ExperienceResponse(ExperienceBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ───────────── Skill ─────────────

class SkillBase(BaseModel):
    name: str
    category: str
    proficiency: int  # 1–100

    @field_validator("proficiency")
    @classmethod
    def validate_proficiency(cls, v: int) -> int:
        if not (1 <= v <= 100):
            raise ValueError("proficiency must be between 1 and 100")
        return v


class SkillCreate(SkillBase):
    pass


class SkillUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    proficiency: Optional[int] = None

    @field_validator("proficiency")
    @classmethod
    def validate_proficiency(cls, v: int | None) -> int | None:
        if v is not None and not (1 <= v <= 100):
            raise ValueError("proficiency must be between 1 and 100")
        return v


class SkillResponse(SkillBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
