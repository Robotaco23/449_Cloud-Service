from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Subscription)
async def subscribe(sub: schemas.SubscriptionCreate, db: AsyncSession = Depends(get_db)):
    return await crud.subscribe_user(db, sub)

@router.get("/{user_id}", response_model=schemas.Subscription)
async def get_subscription(user_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_subscription(db, user_id)

@router.get("/{user_id}/usage")
async def usage_stats(user_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_usage_stats(db, user_id)

@router.put("/{user_id}", response_model=schemas.Subscription)
async def modify_subscription(user_id: int, sub: schemas.SubscriptionCreate, db: AsyncSession = Depends(get_db)):
    return await crud.subscribe_user(db, sub)
