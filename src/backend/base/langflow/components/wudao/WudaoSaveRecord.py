from datetime import timedelta, date

from pymongo.collection import Collection

from langflow.custom import Component
from langflow.inputs import HandleInput
from langflow.io import Output
from langflow.schema.message import Message


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
            name="collection",
            display_name="MongoDB Collection",
            required=True,
            input_types=["Collection"],
            info="The MongoDB Collection",
        ),

    ]

    outputs = [
        Output(display_name="URL", name="url", method="save_data"),
    ]

    def save_data(self) -> Message or None:
        collection = self.collection if isinstance(self.collection, Collection) else self.collection

        # 判断是否有该文件
        query = {
            "title": self.article["title"],
            "type": self.article["type"],
            "time": self.article["time"],
        }
        if collection.find_one(query):
            update_data = {
                "update_time": date.today().strftime("%Y-%m-%d"),
                "file.url": self.article["presigned_url"],
            }
            collection.update_one(query, {"$set": update_data})
        else:
            insert_data = {
                "title": self.article["title"],
                "type": self.article["type"],
                "time": self.article["time"],
                "content": self.article["content"],
                "file": {
                    "filename": self.article["title"] + ".pdf",
                    "bucket_name": self.article["bucket_name"],
                    "url": self.article["presigned_url"],
                    "expire_day": (date.today() + timedelta(days=7)).strftime("%Y-%m-%d")
                },
                "create_time": date.today().strftime("%Y-%m-%d"),
                "update_time": date.today().strftime("%Y-%m-%d"),
            }
            collection.insert_one(insert_data)

        self.status = self.article["presigned_url"]
        return Message(text=self.article["presigned_url"])
