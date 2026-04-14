import uuid
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_get_db
from .schemas import (
    ProjectCreate, ProjectUpdate, ProjectResponse,
    ExperienceCreate, ExperienceUpdate, ExperienceResponse,
    SkillCreate, SkillUpdate, SkillResponse,
)
from . import service

router = APIRouter()


# ─────────── Projects ───────────

@router.get("/projects", response_model=List[ProjectResponse], tags=["Portfolio – Projects"])
async def list_projects(db: AsyncSession = Depends(async_get_db)):
    return await service.get_all_projects(db)


@router.get("/projects/{project_id}", response_model=ProjectResponse, tags=["Portfolio – Projects"])
async def get_project(project_id: uuid.UUID, db: AsyncSession = Depends(async_get_db)):
    return await service.get_project_by_id(project_id, db)


@router.post("/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED, tags=["Portfolio – Projects"])
async def create_project(payload: ProjectCreate, db: AsyncSession = Depends(async_get_db)):
    return await service.create_project(payload, db)


@router.patch("/projects/{project_id}", response_model=ProjectResponse, tags=["Portfolio – Projects"])
async def update_project(project_id: uuid.UUID, payload: ProjectUpdate, db: AsyncSession = Depends(async_get_db)):
    return await service.update_project(project_id, payload, db)


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Portfolio – Projects"])
async def delete_project(project_id: uuid.UUID, db: AsyncSession = Depends(async_get_db)):
    await service.delete_project(project_id, db)


# ─────────── Experiences ───────────

@router.get("/experiences", response_model=List[ExperienceResponse], tags=["Portfolio – Experiences"])
async def list_experiences(db: AsyncSession = Depends(async_get_db)):
    return await service.get_all_experiences(db)


@router.get("/experiences/{experience_id}", response_model=ExperienceResponse, tags=["Portfolio – Experiences"])
async def get_experience(experience_id: uuid.UUID, db: AsyncSession = Depends(async_get_db)):
    return await service.get_experience_by_id(experience_id, db)


@router.post("/experiences", response_model=ExperienceResponse, status_code=status.HTTP_201_CREATED, tags=["Portfolio – Experiences"])
async def create_experience(payload: ExperienceCreate, db: AsyncSession = Depends(async_get_db)):
    return await service.create_experience(payload, db)


@router.patch("/experiences/{experience_id}", response_model=ExperienceResponse, tags=["Portfolio – Experiences"])
async def update_experience(experience_id: uuid.UUID, payload: ExperienceUpdate, db: AsyncSession = Depends(async_get_db)):
    return await service.update_experience(experience_id, payload, db)


@router.delete("/experiences/{experience_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Portfolio – Experiences"])
async def delete_experience(experience_id: uuid.UUID, db: AsyncSession = Depends(async_get_db)):
    await service.delete_experience(experience_id, db)


# ─────────── Skills ───────────

@router.get("/skills", response_model=List[SkillResponse], tags=["Portfolio – Skills"])
async def list_skills(db: AsyncSession = Depends(async_get_db)):
    return await service.get_all_skills(db)


@router.get("/skills/{skill_id}", response_model=SkillResponse, tags=["Portfolio – Skills"])
async def get_skill(skill_id: uuid.UUID, db: AsyncSession = Depends(async_get_db)):
    return await service.get_skill_by_id(skill_id, db)


@router.post("/skills", response_model=SkillResponse, status_code=status.HTTP_201_CREATED, tags=["Portfolio – Skills"])
async def create_skill(payload: SkillCreate, db: AsyncSession = Depends(async_get_db)):
    return await service.create_skill(payload, db)


@router.patch("/skills/{skill_id}", response_model=SkillResponse, tags=["Portfolio – Skills"])
async def update_skill(skill_id: uuid.UUID, payload: SkillUpdate, db: AsyncSession = Depends(async_get_db)):
    return await service.update_skill(skill_id, payload, db)


@router.delete("/skills/{skill_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Portfolio – Skills"])
async def delete_skill(skill_id: uuid.UUID, db: AsyncSession = Depends(async_get_db)):
    await service.delete_skill(skill_id, db)
