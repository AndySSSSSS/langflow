from langflow.custom import Component
from langflow.io import StrInput, MessageTextInput, Output
from langflow.utils.wudao.tool_playwright import save_page_pdf


class WudaoSpiderComponent(Component):
    display_name = "Wudao Spider"
    description = "网页爬取，获取文章信息（标题、时间、文本、类型、pdf bytes）。@五道科技"
    icon = "monitor-down"
    name = "WudaoSpider"

    inputs = [
        MessageTextInput(
            name="url",
            display_name="URL",
            required=True,
            info="The URL to scrape or crawl",
        ),
        StrInput(
            name="type",
            display_name="File Type",
            value='供销新闻',
            required=True,
            info="File type of the file you download.",
        ),
    ]

    outputs = [
        Output(display_name="article", name="article", method="save_page_data"),
    ]

    async def save_page_data(self) -> dict:
        article = await save_page_pdf(self.url)
        article['type'] = self.type
        self.status = article['title']
        return article
