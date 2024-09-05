import json
from typing import List

from langchain_core.prompts import PromptTemplate

from langflow.base.wudao_constants import PROMPT_TEXT_TO_QA
from langflow.custom import Component
from langflow.io import DataInput, HandleInput, Output


class WudaoTextToQAComponent(Component):
    display_name = "Wudao Text To QA"
    description = "将List[str],转化为QA。@五道科技"
    icon = "braces"
    name = "WudaoTextToQA"

    inputs = [
        DataInput(name="data", display_name="Data", input_types=["Text"], info="The data to convert to text."),
        HandleInput(name="llm", display_name="Language Model", input_types=["LanguageModel"], required=True),
    ]

    outputs = [
        Output(display_name="Chunks", name="chunks", method="parse_data"),
    ]

    def parse_data(self) -> List[str]:
        data = self.data if isinstance(self.data, list) else [self.data]
        chunks = []
        count = 1
        all_count = len(data)
        for text in data:
            sequence = PromptTemplate(template=PROMPT_TEXT_TO_QA, input_variables=["text"]) | self.llm
            result = sequence.invoke(text).content
            print(str(count) + "/" + str(all_count))
            count += 1
            chunks.extend(json.loads(result))
        self.status = chunks
        return chunks
