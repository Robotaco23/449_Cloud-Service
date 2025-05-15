from fastapi import FastAPI
from app.routers import plans, permissions, subscriptions, usage, access_control
from app.database import engine, Base

# Initialize database tables
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI(title="Cloud Service Access Management System")

@app.on_event("startup")
async def on_startup():
    await init_db()

app.include_router(plans.router, prefix="/plans", tags=["plans"])
app.include_router(permissions.router, prefix="/permissions", tags=["permissions"])
app.include_router(subscriptions.router, prefix="/subscriptions", tags=["subscriptions"])
app.include_router(usage.router, prefix="/usage", tags=["usage"])
app.include_router(access_control.router, prefix="/access", tags=["access_control"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Cloud Service Access Management System"}
