import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from .models import Project, Experience, Skill
from .schemas import (
    ProjectCreate, ProjectUpdate,
    ExperienceCreate, ExperienceUpdate,
    SkillCreate, SkillUpdate,
)


# ───────────── Project Service ─────────────

async def get_all_projects(db: AsyncSession) -> List[Project]:
    result = await db.execute(select(Project).order_by(Project.created_at.desc()))
    return list(result.scalars().all())


async def get_project_by_id(project_id: uuid.UUID, db: AsyncSession) -> Project:
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


async def create_project(data: ProjectCreate, db: AsyncSession) -> Project:
    project = Project(**data.model_dump())
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project


async def update_project(project_id: uuid.UUID, data: ProjectUpdate, db: AsyncSession) -> Project:
    project = await get_project_by_id(project_id, db)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(project, field, value)
    await db.commit()
    await db.refresh(project)
    return project


async def delete_project(project_id: uuid.UUID, db: AsyncSession) -> None:
    project = await get_project_by_id(project_id, db)
    await db.delete(project)
    await db.commit()


# ───────────── Experience Service ─────────────

async def get_all_experiences(db: AsyncSession) -> List[Experience]:
    result = await db.execute(select(Experience).order_by(Experience.start_date.desc()))
    return list(result.scalars().all())


async def get_experience_by_id(experience_id: uuid.UUID, db: AsyncSession) -> Experience:
    result = await db.execute(select(Experience).where(Experience.id == experience_id))
    experience = result.scalar_one_or_none()
    if not experience:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experience not found")
    return experience


async def create_experience(data: ExperienceCreate, db: AsyncSession) -> Experience:
    experience = Experience(**data.model_dump())
    db.add(experience)
    await db.commit()
    await db.refresh(experience)
    return experience


async def update_experience(experience_id: uuid.UUID, data: ExperienceUpdate, db: AsyncSession) -> Experience:
    experience = await get_experience_by_id(experience_id, db)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(experience, field, value)
    await db.commit()
    await db.refresh(experience)
    return experience


async def delete_experience(experience_id: uuid.UUID, db: AsyncSession) -> None:
    experience = await get_experience_by_id(experience_id, db)
    await db.delete(experience)
    await db.commit()


# ───────────── Skill Service ─────────────

async def get_all_skills(db: AsyncSession) -> List[Skill]:
    result = await db.execute(select(Skill).order_by(Skill.category, Skill.name))
    return list(result.scalars().all())


async def get_skill_by_id(skill_id: uuid.UUID, db: AsyncSession) -> Skill:
    result = await db.execute(select(Skill).where(Skill.id == skill_id))
    skill = result.scalar_one_or_none()
    if not skill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")
    return skill


async def create_skill(data: SkillCreate, db: AsyncSession) -> Skill:
    existing = await db.execute(select(Skill).where(Skill.name == data.name))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Skill already exists")
    skill = Skill(**data.model_dump())
    db.add(skill)
    await db.commit()
    await db.refresh(skill)
    return skill


async def update_skill(skill_id: uuid.UUID, data: SkillUpdate, db: AsyncSession) -> Skill:
    skill = await get_skill_by_id(skill_id, db)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(skill, field, value)
    await db.commit()
    await db.refresh(skill)
    return skill


async def delete_skill(skill_id: uuid.UUID, db: AsyncSession) -> None:
    skill = await get_skill_by_id(skill_id, db)
    await db.delete(skill)
    await db.commit()
