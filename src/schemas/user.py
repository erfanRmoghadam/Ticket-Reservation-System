from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    full_name: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime


class UserUpdateRequest(BaseModel):
    full_name: str | None = None


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
