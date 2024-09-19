from minio import Minio
from pymongo import MongoClient

from langflow.base.logger.index import AsyncLogger
from langflow.custom import Component
from langflow.io import MessageTextInput, HandleInput, StrInput, Output

from langflow.utils.wudao.tool_playwright import save_page_pdf


class WudaoSpiderComponent(Component):
    display_name = "Wudao Spider"
    description = "网页爬取，获取文章信息（标题、时间、文本、类型、pdf bytes）。@五道科技"
    icon = "monitor-down"
    name = "WudaoSpider"

    inputs = [
        MessageTextInput(
            name="aid",
            display_name="The aid fo article",
            info="The aid to scrape or crawl",
            required=True,
        ),
        StrInput(
            name="bucket_name",
            display_name="Bucket name of MinIO",
            required=True,
            value="files",
        ),
        HandleInput(
            name="minio",
            display_name="MinIO",
            required=True,
            input_types=["Minio"],
            info="The MinIO",
        ),
        HandleInput(
            name="mongo",
            display_name="MongoClient",
            required=True,
            input_types=["MongoClient"],
            info="The MongoClient",
        ),
    ]

    outputs = [
        Output(display_name="article", name="article", method="save_page_data"),
    ]

    async def save_page_data(self) -> dict:
        minio = self.minio if isinstance(self.minio, Minio) else self.minio
        mongo = self.mongo if isinstance(self.mongo, MongoClient) else self.mongo
        # 爬取新闻地址
        aid = self.aid
        # minIo bucket name
        bucket_name = self.bucket_name

        # check 文章是否已经下载过
        collection = mongo['files']
        article_mongo = collection.find_one({'aid': aid})
        if article_mongo is not None:
            AsyncLogger.log(f"该网页已下载:[{aid}]")
            return {'error': '该网页已下载。'}

        url = f'https://www.chinacoop.gov.cn/news.html?aid={aid}'

        AsyncLogger.log(f"Start Saving article [{aid}]")
        # 获取文章
        article = await save_page_pdf(url, minio, bucket_name)
        article["bucket_name"] = bucket_name
        self.status = url
        return article
