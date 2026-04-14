import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from .models import Course, Section, Lesson
from .schemas import (
    CourseCreate, CourseUpdate,
    SectionCreate, SectionUpdate,
    LessonCreate, LessonUpdate,
)


# ───────────── Course Service ─────────────

async def get_all_courses(db: AsyncSession) -> List[Course]:
    result = await db.execute(
        select(Course)
        .options(selectinload(Course.sections).selectinload(Section.lessons))
        .order_by(Course.created_at.desc())
    )
    return list(result.scalars().all())


async def get_course_by_id(course_id: uuid.UUID, db: AsyncSession) -> Course:
    result = await db.execute(
        select(Course)
        .options(selectinload(Course.sections).selectinload(Section.lessons))
        .where(Course.id == course_id)
    )
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course


async def create_course(data: CourseCreate, db: AsyncSession) -> Course:
    course = Course(**data.model_dump())
    db.add(course)
    await db.commit()
    await db.refresh(course)
    return await get_course_by_id(course.id, db)


async def update_course(course_id: uuid.UUID, data: CourseUpdate, db: AsyncSession) -> Course:
    course = await get_course_by_id(course_id, db)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(course, field, value)
    await db.commit()
    return await get_course_by_id(course_id, db)


async def delete_course(course_id: uuid.UUID, db: AsyncSession) -> None:
    course = await get_course_by_id(course_id, db)
    await db.delete(course)
    await db.commit()


# ───────────── Section Service ─────────────

async def _get_section(section_id: uuid.UUID, db: AsyncSession) -> Section:
    result = await db.execute(
        select(Section)
        .options(selectinload(Section.lessons))
        .where(Section.id == section_id)
    )
    section = result.scalar_one_or_none()
    if not section:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Section not found")
    return section


async def get_sections_for_course(course_id: uuid.UUID, db: AsyncSession) -> List[Section]:
    await get_course_by_id(course_id, db)  # validates course exists
    result = await db.execute(
        select(Section)
        .options(selectinload(Section.lessons))
        .where(Section.course_id == course_id)
        .order_by(Section.order)
    )
    return list(result.scalars().all())


async def create_section(course_id: uuid.UUID, data: SectionCreate, db: AsyncSession) -> Section:
    await get_course_by_id(course_id, db)
    section = Section(course_id=course_id, **data.model_dump())
    db.add(section)
    await db.commit()
    return await _get_section(section.id, db)


async def update_section(section_id: uuid.UUID, data: SectionUpdate, db: AsyncSession) -> Section:
    section = await _get_section(section_id, db)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(section, field, value)
    await db.commit()
    return await _get_section(section_id, db)


async def delete_section(section_id: uuid.UUID, db: AsyncSession) -> None:
    section = await _get_section(section_id, db)
    await db.delete(section)
    await db.commit()


# ───────────── Lesson Service ─────────────

async def _get_lesson(lesson_id: uuid.UUID, db: AsyncSession) -> Lesson:
    result = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
    lesson = result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")
    return lesson


async def get_lessons_for_section(section_id: uuid.UUID, db: AsyncSession) -> List[Lesson]:
    await _get_section(section_id, db)  # validates section exists
    result = await db.execute(
        select(Lesson).where(Lesson.section_id == section_id).order_by(Lesson.order)
    )
    return list(result.scalars().all())


async def create_lesson(section_id: uuid.UUID, data: LessonCreate, db: AsyncSession) -> Lesson:
    await _get_section(section_id, db)
    lesson = Lesson(section_id=section_id, **data.model_dump())
    db.add(lesson)
    await db.commit()
    await db.refresh(lesson)
    return lesson


async def update_lesson(lesson_id: uuid.UUID, data: LessonUpdate, db: AsyncSession) -> Lesson:
    lesson = await _get_lesson(lesson_id, db)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(lesson, field, value)
    await db.commit()
    await db.refresh(lesson)
    return lesson


async def delete_lesson(lesson_id: uuid.UUID, db: AsyncSession) -> None:
    lesson = await _get_lesson(lesson_id, db)
    await db.delete(lesson)
    await db.commit()
