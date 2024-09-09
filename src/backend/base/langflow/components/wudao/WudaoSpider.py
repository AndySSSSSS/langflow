from typing import List

from langflow.custom import Component
from langflow.utils.tool_playwright import fetch_webpage_content
from langflow.io import StrInput, FileInput, Output


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
        FileInput(name="path", display_name="Save Path", required=True),
    ]

    outputs = [
        Output(display_name="Chunks", name="chunks", method="parse_data"),
    ]

    async def parse_data(self) -> List[str]:
        chunks = []
        text = await fetch_webpage_content(self.url)
        chunks.append(text)
        self.status = chunks
        return chunks
