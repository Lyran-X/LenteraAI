import uuid
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRole(str, Enum):
    STUDENT = "student"
    ADMIN = "admin"
    TEACHER = "teacher"


class UserBase(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)
    role: UserRole = UserRole.STUDENT


class UserPublic(UserBase):
    id: uuid.UUID
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


UserRead = UserPublic