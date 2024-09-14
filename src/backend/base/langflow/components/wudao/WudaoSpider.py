from datetime import timedelta
from io import BytesIO

from minio import Minio

from langflow.custom import Component
from langflow.io import StrInput, MessageTextInput, HandleInput,DataInput, Output
from langflow.schema import Data
from langflow.utils.wudao.tool_playwright import save_page_pdf


class WudaoSpiderComponent(Component):
    display_name = "Wudao Spider"
    description = "网页爬取，获取文章信息（标题、时间、文本、类型、pdf bytes）。@五道科技"
    icon = "monitor-down"
    name = "WudaoSpider"

    inputs = [
        DataInput(
            name="data",
            display_name="Parameters",
            required=True,
            info="aid, bucket_name, bucket_name",
        ),
        HandleInput(
            name="minio",
            display_name="MinIO",
            required=True,
            input_types=["Minio"],
            info="The MinIO",
        ),
        MessageTextInput(
            name="aid",
            display_name="Aid fo news to crawl",
            info="The aid to scrape or crawl",
            advanced=True,
        ),
        MessageTextInput(
            name="bucket_name",
            display_name="Bucket of MinIO",
            advanced=True,
        ),
        MessageTextInput(
            name="type",
            display_name="Column Type",
            info="Column type of the article you download.",
            advanced=True,
        ),
    ]

    outputs = [
        Output(display_name="article", name="article", method="save_page_data"),
    ]

    async def save_page_data(self) -> dict:
        minio = self.minio if isinstance(self.minio, Minio) else self.minio
        # 爬取新闻地址
        aid = self.data.aid if isinstance(self.data, Data) else self.aid
        # minIo bucket name
        bucket_name = self.data.bucket_name if isinstance(self.data, Data) else self.bucket_name
        # 文章类型，column name
        type = self.data.type if isinstance(self.data, Data) else self.type

        url = f'https://www.chinacoop.gov.cn/news.html?aid={aid}'

        # 获取文章
        article = await save_page_pdf(url, minio, bucket_name)
        article["bucket_name"] = bucket_name
        article["type"] = type
        self.status = article['title']
        return article
