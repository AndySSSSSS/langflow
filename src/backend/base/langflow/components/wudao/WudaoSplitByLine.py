from typing import List

import spacy

from langflow.custom import Component
from langflow.io import HandleInput, IntInput, Output
from langflow.schema import Data
from langflow.utils.wudao.tool_text import clean_text, create_chunks


class WudaoSplitByLineComponent(Component):
    display_name: str = "Wudao Split By Line"
    description: str = ("将中文文本清洗，切割成语句，再将语句合并成段落。"
                        " @五道科技")
    icon = "scissors-line-dashed"
    name = "WudaoSplitByLine"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.zh_nlp = spacy.load('zh_core_web_sm')

    inputs = [
        HandleInput(
            name="data_inputs",
            display_name="Data Inputs",
            info="The data to split.",
            input_types=["Data"],
            is_list=True,
        ),
        IntInput(
            name="chunk_overlap",
            display_name="Chunk Overlap",
            info="Number of line to overlap between chunks.",
            value=0,
        ),
        IntInput(
            name="chunk_size",
            display_name="Chunk Size",
            info="The maximum number of line in each chunk.",
            value=1,
        ),
    ]

    outputs = [
        Output(display_name="Chunks", name="chunks", method="split_text"),
    ]

    def split_text(self) -> List[str]:
        documents = []
        for _input in self.data_inputs:
            if isinstance(_input, Data):
                documents.append(_input.to_lc_document())

        docs = []
        for doc in documents:
            p = self.zh_nlp(clean_text(doc.page_content))
            for sent in p.sents:
                text = sent.text

                if len(text) > 0:
                    docs.append(text)
        data = create_chunks(docs, chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        self.status = data
        return data
