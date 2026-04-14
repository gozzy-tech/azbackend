import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, field_validator

VALID_LEVELS = {"beginner", "intermediate", "advanced"}


# ───────────── Lesson ─────────────

class LessonBase(BaseModel):
    title: str
    content: Optional[str] = None
    video_url: Optional[str] = None
    duration_minutes: int = 0
    order: int = 0
    is_free_preview: bool = False


class LessonCreate(LessonBase):
    pass


class LessonUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    video_url: Optional[str] = None
    duration_minutes: Optional[int] = None
    order: Optional[int] = None
    is_free_preview: Optional[bool] = None


class LessonResponse(LessonBase):
    id: uuid.UUID
    section_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ───────────── Section ─────────────

class SectionBase(BaseModel):
    title: str
    order: int = 0


class SectionCreate(SectionBase):
    pass


class SectionUpdate(BaseModel):
    title: Optional[str] = None
    order: Optional[int] = None


class SectionResponse(SectionBase):
    id: uuid.UUID
    course_id: uuid.UUID
    lessons: List[LessonResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ───────────── Course ─────────────

class CourseBase(BaseModel):
    title: str
    description: str
    thumbnail_url: Optional[str] = None
    category: str
    price: float = 0.0
    level: str
    is_published: bool = False

    @field_validator("level")
    @classmethod
    def validate_level(cls, v: str) -> str:
        if v not in VALID_LEVELS:
            raise ValueError(f"level must be one of: {', '.join(VALID_LEVELS)}")
        return v


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    level: Optional[str] = None
    is_published: Optional[bool] = None

    @field_validator("level")
    @classmethod
    def validate_level(cls, v: str | None) -> str | None:
        if v is not None and v not in VALID_LEVELS:
            raise ValueError(f"level must be one of: {', '.join(VALID_LEVELS)}")
        return v


class CourseResponse(CourseBase):
    id: uuid.UUID
    sections: List[SectionResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CourseSummaryResponse(CourseBase):
    """Lightweight response without nested sections/lessons."""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
