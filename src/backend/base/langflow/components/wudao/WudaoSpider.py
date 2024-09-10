from typing import List

from langflow.custom import Component
from langflow.io import StrInput, MessageTextInput, Output
from langflow.utils.wudao.tool_playwright import save_page_pdf


class WudaoSpiderComponent(Component):
    display_name = "Wudao Spider"
    description = "网页爬取。@五道科技"
    icon = "monitor-down"
    name = "WudaoSpider"

    inputs = [
        StrInput(
            name="url",
            display_name="URL",
            required=True,
            info="The URL to scrape or crawl",
        ),
        MessageTextInput(
            name="type",
            display_name="File Type",
            value='供销新闻',
            required=True,
            info="File type of the file you download.",
        ),
    ]

    outputs = [
        Output(display_name="Chunks", name="chunks", method="parse_data"),
    ]

    async def parse_data(self) -> List[str]:
        chunks = []
        text = await save_page_pdf(self.url, self.type)
        chunks.append(text)
        self.status = chunks
        return chunks
