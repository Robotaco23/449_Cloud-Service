from sqlalchemy import Column, Integer, String, Text, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

# Association table for many-to-many Plan <-> Permission
plan_permissions = Table(
    "plan_permissions",
    Base.metadata,
    Column("plan_id", ForeignKey("plans.id"), primary_key=True),
    Column("permission_id", ForeignKey("permissions.id"), primary_key=True)
)

class Plan(Base):
    __tablename__ = "plans"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text)
    usage_limit = Column(Integer, default=0)
    permissions = relationship("Permission", secondary=plan_permissions, back_populates="plans")

class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    endpoint = Column(String, unique=True, nullable=False)
    description = Column(Text)
    plans = relationship("Plan", secondary=plan_permissions, back_populates="permissions")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, default="customer")  # 'admin' or 'customer'
    subscription = relationship("Subscription", back_populates="user", uselist=False)

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    plan_id = Column(Integer, ForeignKey("plans.id"))
    user = relationship("User", back_populates="subscription")
    plan = relationship("Plan")
    usage = relationship("Usage", back_populates="subscription")

class Usage(Base):
    __tablename__ = "usage"
    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"))
    endpoint = Column(String)
    count = Column(Integer, default=0)
    subscription = relationship("Subscription", back_populates="usage")
