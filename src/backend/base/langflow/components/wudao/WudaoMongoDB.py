from pymongo import MongoClient

from langflow.custom import Component
from langflow.io import StrInput, IntInput, Output


class WudaoMongoDBComponent(Component):
    display_name = "Wudao MongoDB"
    description = "MongoDB 是一种流行的NoSQL数据库，它采用面向文档的方式来存储和管理数据。@五道科技"
    icon = "archive"
    name = "WudaoMongoDB"

    inputs = [
        StrInput(
            name="host",
            display_name="MongoDB Host",
            required=True,
            value="localhost",
        ),
        IntInput(
            name="port",
            display_name="MongoDB Port",
            required=True,
            value=17017,
        ),
        StrInput(
            name="database_name",
            display_name="MongoDB Database",
            required=True,
            value="gx",
            info="数据库名",
        ),
        StrInput(
            name="username",
            display_name="MongoDB Username",
            required=True,
            value="admin",
        ),
        StrInput(
            name="password",
            display_name="MongoDB Password",
            required=True,
            value="admin123",
        ),
    ]

    outputs = [
        Output(display_name="MongoDB", name="mongodb", method="get_mongodb"),
    ]

    def get_mongodb(self) -> MongoClient:
        # 构建 MongoDB 连接字符串
        uri = f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}"

        # 连接到 MongoDB
        client = MongoClient(uri)

        # 选择数据库和集合
        db = client[self.database_name]

        self.status = uri

        return db
