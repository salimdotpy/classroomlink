
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.models.enums import UserRole


class UserRegister(BaseModel):
    """
    Data required to register a new lecturer account.
    """

    email: EmailStr
    password: str = Field(
        min_length=12,
        max_length=128,
    )
    model_config = ConfigDict(extra="forbid")

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Password cannot contain only whitespace.")

        # Do not strip the password itself. Spaces can be
        # legitimate parts of a user's password.
        return value


class UserRead(BaseModel):
    """
    Public representation of a ClassroomLink user.

    Password hashes are deliberately excluded.
    """

    id: UUID
    email: EmailStr
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
