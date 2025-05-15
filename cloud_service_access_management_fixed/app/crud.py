from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from app import models, schemas
from fastapi import HTTPException, status

# Plan CRUD
async def create_plan(db: AsyncSession, plan: schemas.PlanCreate):
    db_plan = models.Plan(name=plan.name, description=plan.description, usage_limit=plan.usage_limit)
    if plan.permission_ids:
        perms = await db.execute(select(models.Permission).filter(models.Permission.id.in_(plan.permission_ids)))
        db_plan.permissions = perms.scalars().all()
    db.add(db_plan)
    await db.commit()
    await db.refresh(db_plan)
    return db_plan

async def get_plan(db: AsyncSession, plan_id: int):
    res = await db.execute(select(models.Plan).filter(models.Plan.id == plan_id))
    plan = res.scalars().first()
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    return plan

async def update_plan(db: AsyncSession, plan_id: int, plan_data: schemas.PlanCreate):
    existing = await get_plan(db, plan_id)
    existing.name = plan_data.name
    existing.description = plan_data.description
    existing.usage_limit = plan_data.usage_limit
    if plan_data.permission_ids:
        perms = await db.execute(select(models.Permission).filter(models.Permission.id.in_(plan_data.permission_ids)))
        existing.permissions = perms.scalars().all()
    await db.commit()
    return existing

async def delete_plan(db: AsyncSession, plan_id: int):
    await db.execute(delete(models.Plan).where(models.Plan.id == plan_id))
    await db.commit()
    return {"ok": True}

# Permission CRUD
async def create_permission(db: AsyncSession, perm: schemas.PermissionCreate):
    db_perm = models.Permission(**perm.dict())
    db.add(db_perm)
    await db.commit()
    await db.refresh(db_perm)
    return db_perm

async def get_permission(db: AsyncSession, perm_id: int):
    res = await db.execute(select(models.Permission).filter(models.Permission.id == perm_id))
    perm = res.scalars().first()
    if not perm:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
    return perm

async def update_permission(db: AsyncSession, perm_id: int, perm_data: schemas.PermissionCreate):
    existing = await get_permission(db, perm_id)
    for key, val in perm_data.dict().items(): setattr(existing, key, val)
    await db.commit()
    return existing

async def delete_permission(db: AsyncSession, perm_id: int):
    await db.execute(delete(models.Permission).where(models.Permission.id == perm_id))
    await db.commit()
    return {"ok": True}

# Subscription CRUD
async def subscribe_user(db: AsyncSession, sub: schemas.SubscriptionCreate):
    db_sub = models.Subscription(user_id=sub.user_id, plan_id=sub.plan_id)
    db.add(db_sub)
    await db.commit()
    await db.refresh(db_sub)
    return db_sub

async def get_subscription(db: AsyncSession, user_id: int):
    res = await db.execute(select(models.Subscription).filter(models.Subscription.user_id == user_id))
    sub = res.scalars().first()
    if not sub:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")
    return sub

# Usage Tracking
async def track_usage(db: AsyncSession, user_id: int, endpoint: str):
    sub = await get_subscription(db, user_id)
    res = await db.execute(select(models.Usage).filter(models.Usage.subscription_id == sub.id, models.Usage.endpoint == endpoint))
    u = res.scalars().first()
    if not u:
        u = models.Usage(subscription_id=sub.id, endpoint=endpoint, count=1)
        db.add(u)
    else:
        u.count += 1
    await db.commit()
    await db.refresh(u)
    if u.count > sub.plan.usage_limit:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usage limit exceeded")
    return u

async def get_usage_stats(db: AsyncSession, user_id: int):
    sub = await get_subscription(db, user_id)
    return sub.usage

# Access Control
async def check_access(db: AsyncSession, user_id: int, endpoint: str):
    sub = await get_subscription(db, user_id)
    if endpoint not in [p.endpoint for p in sub.plan.permissions]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
    res = await db.execute(select(models.Usage).filter(models.Usage.subscription_id == sub.id, models.Usage.endpoint == endpoint))
    u = res.scalars().first()
    count = u.count if u else 0
    return {"allowed": count < sub.plan.usage_limit, "used": count, "limit": sub.plan.usage_limit}
