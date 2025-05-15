from typing import List, Optional
from pydantic import BaseModel

class PermissionBase(BaseModel):
    name: str
    endpoint: str
    description: Optional[str]

class PermissionCreate(PermissionBase):
    pass

class Permission(PermissionBase):
    id: int
    class Config:
        orm_mode = True

class PlanBase(BaseModel):
    name: str
    description: Optional[str]
    usage_limit: int

class PlanCreate(PlanBase):
    permission_ids: List[int] = []

class Plan(PlanBase):
    id: int
    permissions: List[Permission] = []
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    role: Optional[str] = "customer"

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    class Config:
        orm_mode = True

class SubscriptionBase(BaseModel):
    user_id: int
    plan_id: int

class SubscriptionCreate(SubscriptionBase):
    pass

class Subscription(SubscriptionBase):
    id: int
    usage: Optional[List[dict]]
    class Config:
        orm_mode = True

class UsageBase(BaseModel):
    endpoint: str

class UsageCreate(UsageBase):
    pass

class Usage(UsageBase):
    count: int
    class Config:
        orm_mode = True
