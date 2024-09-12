import abc
from typing import Optional, Union
from uuid import UUID

from sqlmodel import Session

from langflow.services.base import Service
from langflow.services.database.models.prompt.model import Prompt


class PromptService(Service):
    """
    Abstract base class for a prompt service.
    """

    name = "prompt_service"

    @abc.abstractmethod
    def get_prompt(self, user_id: Union[UUID, str], name: str, field: str, session: Session) -> str:
        """
        Get a prompt value.

        Args:
            user_id: The user ID.
            name: The name of the prompt.
            field: The field of the prompt.
            session: The database session.

        Returns:
            The value of the prompt.
        """

    @abc.abstractmethod
    def list_prompt(self, user_id: Union[UUID, str], session: Session) -> list[Optional[str]]:
        """
        List all prompt.

        Args:
            user_id: The user ID.
            session: The database session.

        Returns:
            A list of prompt names.
        """

    @abc.abstractmethod
    def update_prompt(self, user_id: Union[UUID, str], name: str, content: str, description: str, session: Session) -> Prompt:
        """
        Update a prompt.

        Args:
            user_id: The user ID.
            name: The name of the prompt.
            content: 内容.
            description: 备注.
            session: The database session.

        Returns:
            The updated prompt.
        """

    @abc.abstractmethod
    def delete_prompt(self, user_id: Union[UUID, str], name: str, session: Session) -> None:
        """
        Delete a prompt.

        Args:
            user_id: The user ID.
            name: The name of the prompt.
            session: The database session.

        Returns:
            The deleted prompt.
        """

    @abc.abstractmethod
    def delete_prompt_by_id(self, user_id: Union[UUID, str], prompt_id: UUID, session: Session) -> None:
        """
        Delete a prompt by ID.

        Args:
            user_id: The user ID.
            prompt_id: The ID of the prompt.
            session: The database session.
        """

    @abc.abstractmethod
    def create_prompt(
        self,
        user_id: Union[UUID, str],
        name: str,
        content: str,
        description: str,
        session: Session,
    ) -> Prompt:
        """
        Create a prompt.

        Args:
            user_id: The user ID.
            name: The name of the prompt.
            content: 内容.
            description: 备注.
            session: The database session.

        Returns:
            The created prompt.
        """
