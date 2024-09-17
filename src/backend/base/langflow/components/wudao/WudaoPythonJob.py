import asyncio
import os
import subprocess
import tempfile
from typing import List

from langflow.custom import Component
from langflow.io import CodeInput, Output
from langflow.schema import Data, dotdict


class WudaoPythonJobComponent(Component):
    display_name = "Wudao Python Job"
    description = "Define and execute a Python job that returns a Data or List[Data]."
    icon = "Python"
    name = "WudaoPythonJob"

    inputs = [
        CodeInput(
            name="function_code",
            display_name="Function Code",
            info="The code for the function.",
        ),
    ]

    outputs = [
        Output(
            name="function_output_data",
            display_name="Function Output (Data)",
            method="execute_function_data",
        ),
    ]

    # 使用异步方式来执行命令并实时打印输出
    async def execute_and_print(self, function_code):
        # 创建一个临时文件来保存代码
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
            temp_file.write(function_code.encode())
            temp_file.flush()
            temp_file_path = temp_file.name

        # 使用 python 执行临时文件
        process = await asyncio.create_subprocess_exec(
            'python', temp_file_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={**os.environ, "PYTHONUNBUFFERED": "1"}  # 禁用缓冲
        )

        lines = []
        while True:
            line = await process.stdout.readline()
            if line == b'':
                break
            print(line.decode().rstrip())
            lines.append(line.decode().rstrip())

        # 读取错误输出
        while True:
            error_line = await process.stderr.readline()
            if error_line == b'':
                break
            print("ERROR:", error_line.decode().rstrip())
            lines.append("ERROR: " + error_line.decode().rstrip())

        await process.wait()
        return_code = process.returncode

        # 清理临时文件
        os.remove(temp_file_path)

        return lines if return_code == 0 else return_code

    async def execute_function(self) -> List[dotdict | str] | dotdict | str:
        function_code = self.function_code

        if not function_code:
            return "No function code provided."

        try:
            # 使用 await 来调用异步的执行函数
            lines = await self.execute_and_print(function_code)

            return lines
        except Exception as e:
            return f"Error executing function: {str(e)}"

    async def execute_function_data(self) -> Data or List[Data]:
        results = await self.execute_function()  # 直接使用 await 而不是 asyncio.run
        results = results if isinstance(results, list) else [results]
        data = [(Data(text=str(x)) if isinstance(x, str) or isinstance(x, int) else Data(**x)) for x in results]
        return data
