from minio import Minio

from langflow.custom import Component
from langflow.io import StrInput, BoolInput, Output


class WudaoMinioComponent(Component):
    display_name = "Wudao Minio"
    description = "MinIO 是一款高性能、分布式的对象存储系统。@五道科技"
    icon = "warehouse"
    name = "WudaoMinio"

    inputs = [
        StrInput(
            name="endpoint",
            display_name="endpoint",
            required=True,
            value="localhost:9000",
            info="MinIO 服务器地址",
        ),
        StrInput(
            name="access_key",
            display_name="Access Key",
            required=True,
            value="v0OpOhLUzqM4dFxz",
            info="MinIO 的 Access Key",
        ),
        StrInput(
            name="secret_key",
            display_name="Secret Key",
            required=True,
            value="i2L1tubSbsVgdk7sTyU3bcPedxaVhPBk",
            info="MinIO 的 Secret Key",
        ),
        BoolInput(
            name="secure",
            display_name="SSL",
            required=True,
            value=False,
            info="如果使用的是 HTTP 而非 HTTPS，设置为 False",
        ),

    ]

    outputs = [
        Output(display_name="MinIO", name="minio", method="get_minio"),
    ]

    async def get_minio(self) -> object:
        minio_client = Minio(
            self.endpoint,  # 替换为 MinIO 服务器地址
            access_key=self.access_key,  # 替换为 MinIO 的 Access Key
            secret_key=self.secret_key,  # 替换为 MinIO 的 Secret Key
            secure=self.secure  # 如果使用的是 HTTP 而非 HTTPS，设置为 False
        )
        self.status = self.endpoint
        return minio_client
