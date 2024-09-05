from typing import List

from langflow.custom import Component
from langflow.io import HandleInput, IntInput, MessageTextInput, Output,MultilineInput
from langflow.schema import Data
import spacy
import re


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

    def create_chunks(self, docs):
        # 初始化 chunks 列表和当前索引
        chunks = []
        start_idx = 0

        while start_idx < len(docs):
            # 计算当前 chunk 的结束索引
            end_idx = start_idx + self.chunk_size
            # 获取当前 chunk 的字符串列表
            chunk = docs[start_idx:end_idx]
            # 将 chunk 转换为单个字符串并添加到 chunks 列表
            chunks.append(''.join(chunk))
            # 更新下一个 chunk 的开始索引
            # 确保下一个 chunk 从前一个 chunk 的末尾向前 chunk_overlap 个字符串开始
            start_idx = end_idx - self.chunk_overlap

        return chunks

    def clean_text(self, text):
        # 去除 HTML 标签
        text = re.sub(r'<[^>]+>', '', text)
        # 去除网页中的空白符号
        text = re.sub(r'&nbsp;', ' ', text)
        # 去除换行符和回车符
        text = re.sub(r'[\n\r]', '', text)
        # 去除乱码字符（如�、￾等不可见字符），匹配 Unicode 控制字符和特殊符号
        text = re.sub(r'[\uFFFD\uFEFF\ufffc\ufff0-\uffff]', '', text)
        # 去除乱码字符（如非中文、英文、数字、标点符号的字符）
        text = re.sub(r'[^\u4e00-\u9fff\w\s,.，。！？]', '', text)
        # 去除多余的空格
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def split_text(self) -> List[str]:
        documents = []
        for _input in self.data_inputs:
            if isinstance(_input, Data):
                documents.append(_input.to_lc_document())

        docs = []
        for doc in documents:
            p = self.zh_nlp(self.clean_text(doc.page_content))
            for sent in p.sents:
                text = sent.text

                if len(text) > 0:
                    docs.append(text)
        data = self.create_chunks(docs)
        self.status = data
        return data
