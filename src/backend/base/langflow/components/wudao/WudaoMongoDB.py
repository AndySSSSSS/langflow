from langflow.custom import Component
from langflow.io import StrInput, IntInput, SecretStrInput, Output


class WudaoMongoDBComponent(Component):
    display_name = "Wudao MongoDB"
    description = "MongoDB 是一种流行的NoSQL数据库，它采用面向文档的方式来存储和管理数据。@五道科技"
    icon = "archive"
    name = "WudaoMongoDB"

    inputs = [
        StrInput(
            name="ip",
            display_name="IP",
            required=True,
            value="localhost",
        ),
        IntInput(
            name="port",
            display_name="Port",
            required=True,
            value=17017,
        ),
        StrInput(
            name="database",
            display_name="Database",
            required=True,
            value="gx",
            info="数据库名",
        ),
        StrInput(
            name="collection",
            display_name="Collection",
            required=True,
            value="files",
            info="文档名",
        ),
        StrInput(
            name="username",
            display_name="Username",
            required=True,
            value="admin",
        ),
        SecretStrInput(
            name="password",
            display_name="Password",
            required=True,
            value="admin123",
        ),
    ]

    outputs = [
        Output(display_name="MongoDB", name="mongodb", method="get_mongodb"),
    ]

    def get_mongodb(self) -> object:
        # # 连接到MongoDB
        # client = MongoClient(self.ip, self.port)
        #
        # # 连接到指定的数据库并进行认证
        # db = client[self.database]
        # db.authenticate(self.username, self.password)
        #
        # # 现在可以对数据库进行操作了
        # collection = db[self.collection]
        #
        # self.status = self.ip + ":" + str(self.port) + "/" + self.endpoint
        #
        # return collection

        try:
            from pymongo import MongoClient
        except ImportError:
            raise ImportError("Please install pymongo to use MongoDB Atlas Vector Store")

        try:
            mongo_client: MongoClient = MongoClient(self.ip, self.port)
            collection = mongo_client[self.database][self.collection]
            if collection:
                self.status = self.ip + ":" + str(self.port) + "/" + self.endpoint
                # 查询所有文档
                results = collection.find()

                # 遍历查询结果
                for doc in results:
                    print(doc)
                return collection
        except Exception as e:
            raise ValueError(f"Failed to connect to MongoDB Atlas: {e}")

        return None
