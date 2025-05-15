from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud
from app.database import get_db

router = APIRouter()

@router.get("/{user_id}/{endpoint}")
async def access(user_id: int, endpoint: str, db: AsyncSession = Depends(get_db)):
    return await crud.check_access(db, user_id, endpoint)
