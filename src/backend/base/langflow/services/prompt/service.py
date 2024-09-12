import os
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional, Union
from uuid import UUID

from fastapi import Depends
from loguru import logger
from sqlmodel import Session, select

from langflow.services.auth import utils as auth_utils
from langflow.services.base import Service
from langflow.services.database.models.prompt.model import Prompt, PromptCreate, PromptUpdate
from langflow.services.deps import get_session
from langflow.services.prompt.base import PromptService

if TYPE_CHECKING:
    from langflow.services.settings.service import SettingsService

CREDENTIAL_TYPE = "Credential"
GENERIC_TYPE = "Generic"


class DatabasePromptService(PromptService, Service):
    def __init__(self, settings_service: "SettingsService"):
        self.settings_service = settings_service

    def get_prompt(
        self,
        user_id: Union[UUID, str],
        name: str,
        session: Session = Depends(get_session),
    ) -> Optional[Prompt]:
        # we get the credential from the database
        # credential = session.query(Prompt).filter(Prompt.user_id == user_id, Prompt.name == name).first()
        prompt = session.exec(select(Prompt).where(Prompt.user_id == user_id, Prompt.name == name)).first()

        if not prompt:
            raise ValueError(f"{name} prompt not found.")

        return prompt

    def get_all(self, user_id: Union[UUID, str], session: Session = Depends(get_session)) -> list[Optional[Prompt]]:
        return list(session.exec(select(Prompt).where(Prompt.user_id == user_id)).all())

    def list_prompt(self, user_id: Union[UUID, str], session: Session = Depends(get_session)) -> list[Optional[str]]:
        prompt_list = self.get_all(user_id=user_id, session=session)
        return [prompt.name for prompt in prompt_list if prompt]

    def update_prompt(
        self,
        user_id: Union[UUID, str],
        name: str,
        content: str,
        description: str,
        session: Session = Depends(get_session),
    ):
        prompt = session.exec(select(Prompt).where(Prompt.user_id == user_id, Prompt.name == name)).first()
        if not prompt:
            raise ValueError(f"{name} prompt not found.")
        prompt.content = content
        prompt.description = description
        session.add(prompt)
        session.commit()
        session.refresh(prompt)
        return prompt

    def update_prompt_fields(
        self,
        user_id: Union[UUID, str],
        prompt_id: Union[UUID, str],
        prompt: PromptUpdate,
        session: Session = Depends(get_session),
    ):
        exist_prompt = session.exec(select(Prompt).where(Prompt.name == prompt.name, Prompt.id != prompt_id)).all()
        if exist_prompt:
            raise ValueError("名称已存在.")

        query = select(Prompt).where(Prompt.id == prompt_id, Prompt.user_id == user_id)
        db_prompt = session.exec(query).one()

        prompt_data = prompt.model_dump(exclude_unset=True)
        for key, value in prompt_data.items():
            setattr(db_prompt, key, value)
        db_prompt.updated_at = datetime.now(timezone.utc)

        session.add(db_prompt)
        session.commit()
        session.refresh(db_prompt)
        return db_prompt

    def delete_prompt(
        self,
        user_id: Union[UUID, str],
        name: str,
        session: Session = Depends(get_session),
    ):
        stmt = select(Prompt).where(Prompt.user_id == user_id).where(Prompt.name == name)
        prompt = session.exec(stmt).first()
        if not prompt:
            raise ValueError(f"{name} prompt not found.")
        session.delete(prompt)
        session.commit()

    def delete_prompt_by_id(self, user_id: Union[UUID, str], prompt_id: UUID, session: Session):
        prompt = session.exec(select(Prompt).where(Prompt.user_id == user_id, Prompt.id == prompt_id)).first()
        if not prompt:
            raise ValueError(f"{prompt_id} prompt not found.")
        session.delete(prompt)
        session.commit()

    def create_prompt(
        self,
        user_id: Union[UUID, str],
        name: str,
        content: str,
        description: str,
        session: Session = Depends(get_session),
    ):
        prompt_base = PromptCreate(
            name=name,
            content=content,
            description=description,
        )
        prompt = Prompt.model_validate(prompt_base, from_attributes=True, update={"user_id": user_id})
        session.add(prompt)
        session.commit()
        session.refresh(prompt)
        return prompt
