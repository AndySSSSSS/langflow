from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy import delete
from sqlmodel import Session

from langflow.services.auth.utils import get_current_active_user
from langflow.services.database.models.user.model import User
from langflow.services.database.models.prompt import Prompt, PromptCreate, PromptRead, PromptUpdate
from langflow.services.deps import get_session, get_prompt_service
from langflow.services.prompt.service import DatabasePromptService

router = APIRouter(prefix="/prompt", tags=["Prompt"])


@router.post("/", response_model=PromptRead, status_code=201)
def create_prompt(
    *,
    session: Session = Depends(get_session),
    prompt: PromptCreate,
    current_user: User = Depends(get_current_active_user),
    prompt_service: DatabasePromptService = Depends(get_prompt_service),
):
    """Create a new prompt."""
    try:
        if not prompt.name and not prompt.content:
            raise HTTPException(status_code=400, detail="名称和内容不能为空")

        if not prompt.name:
            raise HTTPException(status_code=400, detail="名称不能为空")

        if not prompt.content:
            raise HTTPException(status_code=400, detail="内容不能为空")

        if prompt.name in prompt_service.list_prompt(user_id=current_user.id, session=session):
            raise HTTPException(status_code=400, detail="名称已经存在")

        return prompt_service.create_prompt(
            user_id=current_user.id,
            name=prompt.name,
            content=prompt.content,
            description=prompt.description,
            session=session,
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("", response_model=list[PromptRead], status_code=200)
def read_prompt(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
    prompt_service: DatabasePromptService = Depends(get_prompt_service),
):
    """Read all Prompt."""
    try:
        return prompt_service.get_all(user_id=current_user.id, session=session)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.patch("/{prompt_id}", response_model=PromptRead, status_code=200)
def update_prompt(
    *,
    session: Session = Depends(get_session),
    prompt_id: UUID,
    prompt: PromptUpdate,
    current_user: User = Depends(get_current_active_user),
    prompt_service: DatabasePromptService = Depends(get_prompt_service),
):
    """Update a prompt."""
    try:
        return prompt_service.update_prompt_fields(
            user_id=current_user.id,
            prompt_id=prompt_id,
            prompt=prompt,
            session=session,
        )
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Prompt not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("", status_code=204)
async def delete_prompt(
    prompt_ids: list[UUID],
    session: Session = Depends(get_session),
):
    try:
        session.exec(delete(Prompt).where(Prompt.id.in_(prompt_ids)))  # type: ignore
        session.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
