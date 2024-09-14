import asyncio
import subprocess
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
    async def execute_and_print(self, command):
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={**subprocess.os.environ, "PYTHONUNBUFFERED": "1"}  # 禁用缓冲
        )

        lines = []
        # 实时读取输出
        while True:
            line = await process.stdout.readline()
            if line == b'':
                break
            print(line.decode().rstrip())
            lines.append(line.decode().rstrip())

        # 等待进程结束
        await process.wait()
        return lines

    async def execute_function(self) -> List[dotdict | str] | dotdict | str:
        function_code = self.function_code

        if not function_code:
            return "No function code provided."

        try:
            # 使用三重引号来保证多行代码的正确传递
            command = f'python -c """{function_code}"""'

            # 使用 await 来调用异步的执行函数
            lines = await self.execute_and_print(command)

            return lines
        except Exception as e:
            return f"Error executing function: {str(e)}"

    async def execute_function_data(self) -> Data or List[Data]:
        results = await self.execute_function()  # 直接使用 await 而不是 asyncio.run
        results = results if isinstance(results, list) else [results]
        data = [(Data(text=x) if isinstance(x, str) else Data(**x)) for x in results]
        return data
