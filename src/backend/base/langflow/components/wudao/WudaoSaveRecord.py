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
        article = self.article if isinstance(self.article, dict) else self.article

        if "title" not in article or article["title"] == '':
            return Message(text='无效地址')

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
                "column": {
                    "id": article["column_id"],
                    "type": article["column_type"],
                    "link": article["column_link"],
                },
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

        self.status = article["presigned_url"]
        return Message(text=article["presigned_url"])
