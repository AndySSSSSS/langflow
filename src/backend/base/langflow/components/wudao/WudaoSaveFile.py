from langflow.custom import Component
from langflow.inputs import HandleInput
from langflow.io import StrInput, Output
from pymongo.collection import Collection


class WudaoSaveFileComponent(Component):
    display_name = "Wudao Save File"
    description = "保存文章，并将关键数据存入MongoDB，pdf保存至MinIO。@五道科技"
    icon = "save-all"
    name = "WudaoSaveFile"

    inputs = [
        StrInput(
            name="bucket",
            display_name="Bucket of MinIO",
            value="docs",
            required=True,
            input_types=["str"],
            info="The article to save",
        ),
        HandleInput(
            name="article",
            display_name="Article",
            required=True,
            input_types=["dict"],
            info="The article to save",
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
            display_name="MongoDB Collection",
            required=True,
            input_types=["Collection"],
            info="The MongoDB Collection",
        ),

    ]

    outputs = [
        Output(display_name="Chunks", name="chunks", method="save_data"),
    ]

    def save_data(self) -> str:
        print(type(self.mongo))
        print(type(self.minio))

        self.status = self.article['title']
        return "chunks"
