from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import schemas, models
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Permission])
async def list_permissions(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(models.Permission))
    return res.scalars().all()
