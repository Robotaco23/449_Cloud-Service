from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud
from app.database import get_db

router = APIRouter()

@router.post("/{user_id}")
async def track(user_id: int, endpoint: str, db: AsyncSession = Depends(get_db)):
    return await crud.track_usage(db, user_id, endpoint)

@router.get("/{user_id}/limit")
async def check_limit(user_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.check_access(db, user_id, None)
