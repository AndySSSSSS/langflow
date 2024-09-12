from langflow.services.factory import ServiceFactory
from langflow.services.prompt.service import DatabasePromptService
from langflow.services.settings.service import SettingsService


class PromptServiceFactory(ServiceFactory):
    name = "prompt_service"

    def __init__(self):
        super().__init__(DatabasePromptService)

    def create(self, settings_service: SettingsService):
        return self.service_class(settings_service)
