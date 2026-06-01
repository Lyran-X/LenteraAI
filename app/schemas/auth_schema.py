from pydantic import BaseModel, EmailStr, Field

from app.schemas.user_schema import UserPublic, UserRole


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: UserRole = UserRole.STUDENT


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenResponse(AccessTokenResponse):
    user: UserPublic


class MessageResponse(BaseModel):
    message: str