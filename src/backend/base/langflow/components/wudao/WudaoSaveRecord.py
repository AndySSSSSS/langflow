from datetime import timedelta, date

from langflow.custom import Component
from langflow.inputs import HandleInput
from langflow.io import Output
from langflow.schema.message import Message
from pymongo import MongoClient
from pymongo.collection import Collection


class WudaoSaveRecordComponent(Component):
    display_name = "Wudao Save Record"
    description = "保存文章，并将关键数据存入MongoDB。@五道科技"
    icon = "save-all"
    name = "WudaoSaveRecord"

    inputs = [
        HandleInput(
            name="article",
            display_name="Article",
            required=True,
            input_types=["dict"],
            info="The article to save",
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
        Output(display_name="URL", name="url", method="save_data"),
    ]

    def save_data(self) -> Message or None:
        mongo = self.mongo if isinstance(self.mongo, MongoClient) else self.mongo
        article = self.article if isinstance(self.article, dict) else self.article

        if "error" in article:
            return Message(text=article['error'])

        collection = mongo["files"]
        # 判断是否有该文件
        query = {
            "aid": article["aid"],
        }
        if collection.find_one(query):
            update_data = {
                "update_time": date.today().strftime("%Y-%m-%d"),
                "file.url": article["presigned_url"],
            }
            collection.update_one(query, {"$set": update_data})
        else:
            insert_data = {
                "title": article["title"],
                "aid": article["aid"],
                "type": article["type"],
                "time": article["time"],
                "content": article["content"],
                "file": {
                    "filename": article["title"] + ".pdf",
                    "bucket_name": article["bucket_name"],
                    "url": article["presigned_url"],
                    "expire_day": (date.today() + timedelta(days=7)).strftime("%Y-%m-%d")
                },
                "create_time": date.today().strftime("%Y-%m-%d"),
                "update_time": date.today().strftime("%Y-%m-%d"),
            }
            collection.insert_one(insert_data)

        message = Message(text=article["title"], files=[article["presigned_url"]])
        self.status = message
        return message
