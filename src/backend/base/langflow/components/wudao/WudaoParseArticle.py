from typing import List

from langchain_core.prompts import PromptTemplate

from langflow.custom import Component
from langflow.io import DataInput, HandleInput, Output


class WudaoParseArticleComponent(Component):
    display_name = "Wudao Parse Article"
    description = "整理爬取到的文章内容。@五道科技"
    icon = "notebook-pen"
    name = "WudaoParseArticle"

    inputs = [
        DataInput(name="data", display_name="Data", input_types=["Text"], info="The article to parse."),
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
        PROMPT_PARSE_TEXT = """
请将以下文章严格按照Markdown格式输出，提取以下实体，并**严格保持原文内容不变**：
- **标题**: 原文标题
- **来源**: 文章的来源
- **作者**: 文章的作者
- **发布时间**: 文章的发布时间
- **内容**: 文章主体内容

重要规则：
1. **绝对不允许对原文进行任何改写或摘要**。
2. **只做格式调整**，严格保持原文内容完整性。
3. 如果某个实体为空，则不展示该字段。
4. 实体前使用相应的Markdown标签，格式如下：
   - 标题：`# 标题`
   - 来源：`**来源**: 来源`
   - 作者：`**作者**: 作者`
   - 发布时间：`**发布时间**: 日期`
   - 正文内容直接显示，不要做任何改动。

示例格式：
# 标题
**来源**: 来源名称  
**作者**: 作者姓名  
**发布时间**: 发布时间日期  
正文内容

请处理以下内容：
{text}
                """
        for text in data:
            sequence = PromptTemplate(template=PROMPT_PARSE_TEXT, input_variables=["text"]) | self.llm
            result = sequence.invoke(text).content
            chunks.append(result)
            print(str(count) + "/" + str(all_count))
            count += 1

        self.status = chunks
        return chunks
