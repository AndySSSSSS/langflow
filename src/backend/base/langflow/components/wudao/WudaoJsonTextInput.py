import json

from langflow.base.io.text import TextComponent
from langflow.io import MultilineInput, Output
from langflow.schema import Data


class WudaoJsonTextInputComponent(TextComponent):
    display_name = "Wudao Json Text Input"
    description = "Get json text inputs from the Playground."
    icon = "type"
    name = "WudaoJsonText"

    inputs = [
        MultilineInput(
            name="input_value",
            display_name="Text",
            info="JSON Text to be passed as input.",
        ),
    ]
    outputs = [
        Output(display_name="Data", name="data", method="text_response"),
    ]

    def text_response(self) -> Data:
        data = json.loads(self.input_value)
        return_data = Data(data=data)
        self.status = return_data
        return return_data
