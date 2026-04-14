import uuid
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_get_db
from .schemas import (
    CourseCreate, CourseUpdate, CourseResponse, CourseSummaryResponse,
    SectionCreate, SectionUpdate, SectionResponse,
    LessonCreate, LessonUpdate, LessonResponse,
)
from . import service

router = APIRouter()


# ─────────── Courses ───────────

@router.get("/courses", response_model=List[CourseSummaryResponse], tags=["Courses"])
async def list_courses(db: AsyncSession = Depends(async_get_db)):
    return await service.get_all_courses(db)


@router.get("/courses/{course_id}", response_model=CourseResponse, tags=["Courses"])
async def get_course(course_id: uuid.UUID, db: AsyncSession = Depends(async_get_db)):
    return await service.get_course_by_id(course_id, db)


@router.post("/courses", response_model=CourseResponse, status_code=status.HTTP_201_CREATED, tags=["Courses"])
async def create_course(payload: CourseCreate, db: AsyncSession = Depends(async_get_db)):
    return await service.create_course(payload, db)


@router.patch("/courses/{course_id}", response_model=CourseResponse, tags=["Courses"])
async def update_course(course_id: uuid.UUID, payload: CourseUpdate, db: AsyncSession = Depends(async_get_db)):
    return await service.update_course(course_id, payload, db)


@router.delete("/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Courses"])
async def delete_course(course_id: uuid.UUID, db: AsyncSession = Depends(async_get_db)):
    await service.delete_course(course_id, db)


# ─────────── Sections ───────────

@router.get("/courses/{course_id}/sections", response_model=List[SectionResponse], tags=["Courses – Sections"])
async def list_sections(course_id: uuid.UUID, db: AsyncSession = Depends(async_get_db)):
    return await service.get_sections_for_course(course_id, db)


@router.post("/courses/{course_id}/sections", response_model=SectionResponse, status_code=status.HTTP_201_CREATED, tags=["Courses – Sections"])
async def create_section(course_id: uuid.UUID, payload: SectionCreate, db: AsyncSession = Depends(async_get_db)):
    return await service.create_section(course_id, payload, db)


@router.patch("/sections/{section_id}", response_model=SectionResponse, tags=["Courses – Sections"])
async def update_section(section_id: uuid.UUID, payload: SectionUpdate, db: AsyncSession = Depends(async_get_db)):
    return await service.update_section(section_id, payload, db)


@router.delete("/sections/{section_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Courses – Sections"])
async def delete_section(section_id: uuid.UUID, db: AsyncSession = Depends(async_get_db)):
    await service.delete_section(section_id, db)


# ─────────── Lessons ───────────

@router.get("/sections/{section_id}/lessons", response_model=List[LessonResponse], tags=["Courses – Lessons"])
async def list_lessons(section_id: uuid.UUID, db: AsyncSession = Depends(async_get_db)):
    return await service.get_lessons_for_section(section_id, db)


@router.post("/sections/{section_id}/lessons", response_model=LessonResponse, status_code=status.HTTP_201_CREATED, tags=["Courses – Lessons"])
async def create_lesson(section_id: uuid.UUID, payload: LessonCreate, db: AsyncSession = Depends(async_get_db)):
    return await service.create_lesson(section_id, payload, db)


@router.patch("/lessons/{lesson_id}", response_model=LessonResponse, tags=["Courses – Lessons"])
async def update_lesson(lesson_id: uuid.UUID, payload: LessonUpdate, db: AsyncSession = Depends(async_get_db)):
    return await service.update_lesson(lesson_id, payload, db)


@router.delete("/lessons/{lesson_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Courses – Lessons"])
async def delete_lesson(lesson_id: uuid.UUID, db: AsyncSession = Depends(async_get_db)):
    await service.delete_lesson(lesson_id, db)
