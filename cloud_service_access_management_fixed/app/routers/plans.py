from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Plan)
async def create_plan(plan: schemas.PlanCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_plan(db, plan)

@router.put("/{plan_id}", response_model=schemas.Plan)
async def update_plan(plan_id: int, plan: schemas.PlanCreate, db: AsyncSession = Depends(get_db)):
    return await crud.update_plan(db, plan_id, plan)

@router.delete("/{plan_id}")
async def delete_plan(plan_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_plan(db, plan_id)
