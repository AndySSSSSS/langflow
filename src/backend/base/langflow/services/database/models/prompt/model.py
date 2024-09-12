from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import field_serializer
from sqlmodel import JSON, Column, DateTime, Field, SQLModel, func


def utc_now():
    return datetime.now(timezone.utc)


class PromptBase(SQLModel):
    name: str = Field(description="名称")
    content: str = Field(description="内容")
    description: Optional[str] = Field(description="备注")


class Prompt(PromptBase, table=True):  # type: ignore
    id: Optional[UUID] = Field(
        default_factory=uuid4,
        primary_key=True,
        description="Unique ID for the prompt",
    )
    # name is unique per user
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=True),
        description="Creation time of the prompt",
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True),
        description="Last update time of the prompt",
    )
    # foreign key to user table
    user_id: UUID = Field(description="User ID associated with this prompt", foreign_key="user.id")


class PromptCreate(PromptBase):
    created_at: Optional[datetime] = Field(default_factory=utc_now, description="Creation time of the prompt")

    updated_at: Optional[datetime] = Field(default_factory=utc_now, description="Creation time of the prompt")


class PromptRead(SQLModel):
    id: UUID
    name: Optional[str] = Field(None, description="名称")
    content: Optional[str] = Field(None, description="内容")
    description: Optional[str] = Field(None, description="备注")
    created_at: Optional[datetime] = Field()

    @field_serializer("created_at")
    @classmethod
    def serialize_created_at(cls, v):
        v = v.replace(microsecond=0)
        return v.strftime("%Y-%m-%d %H:%M:%S")


class PromptUpdate(SQLModel):
    name: Optional[str] = Field(None, description="名称")
    content: Optional[str] = Field(None, description="内容")
    description: Optional[str] = Field(None, description="备注")
