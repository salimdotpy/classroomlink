
from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, Enum as SAEnum, String
from sqlmodel import Field

from app.models.base import BaseModel
from app.models.enums import UserRole


class User(BaseModel, table=True):
    """
    ClassroomLink user database entity.

    Supports lecturer and student accounts.
    """

    __tablename__ = "users"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
    )

    email: str = Field(
        sa_column=Column(
            String(255),
            nullable=False,
            unique=True,
            index=True,
        )
    )

    password_hash: str = Field(
        sa_column=Column(
            String(255),
            nullable=False,
        )
    )

    role: UserRole = Field(
        default=UserRole.LECTURER,
        sa_column=Column(
            SAEnum(
                UserRole,
                name="user_role",
                native_enum=False,
                values_callable=lambda enum: [
                    item.value for item in enum
                ],
                length=20,
            ),
            nullable=False,
        ),
    )

    is_active: bool = Field(
        default=True,
        nullable=False,
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),
        nullable=False,
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),
        nullable=False,
        sa_column_kwargs={
            "onupdate": lambda: datetime.now(timezone.utc),
        },
    )
