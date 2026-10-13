import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")
base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

client = OpenAI(api_key=api_key, base_url=base_url)

def calculate(expression: str) -> str:
    """calculate the result of a mathematical expression."""
    try:
        result = eval(expression)
        return json.dumps(
            {"result" : result}
        )
    except Exception as e:
        return json.dumps(
            {"error" : f"计算失败 : {str(e)}"}
        )

def get_system_status() -> str:
    """get the system status."""
    cpu_count = os.cpu_count()
    return json.dumps(
        {
            "os" : "Ubuntu Linux",
            "cpu_cores" : f"{cpu_count} cores",
            "status" : "Running"
        }
    )

class calculateInput(BaseModel):
    expression : str = Field(
        description = "要计算的数学表达式，例如：'2 + 2 * 3'或 '1011 / 11' 或 '2 ** 100'"
    )

class EmptyInput(BaseModel):
    # 这个工具不需要任何参数
    pass

tools = [
    {
        "type" : "function",
        "function" : {
            "name" : "calculate",
            "description" : "数学计算器，要进行数学计算的时候必须调用此工具",
            "parameters" : calculateInput.model_json_schema()
        }
    },
    {
            "type" : "function",
            "function" : {
                "name" : "get_system_status",
                "description" : "获取用户当前电脑硬件信息和系统运行状态是调用此工具",
                "parameters" : EmptyInput.model_json_schema()
            }
        }
]

AVAILABLE_TOOLS = {
    "calculate" : calculate,
    "get_system_status" : get_system_status,
}

user_prompt = "帮我算一下 2048 * 128 等于多少，另外告诉我这台电脑CPU有几个核心？"

messages = [
    {
        "role" : "user",
        "content" : user_prompt
    }
]

first_response = client.chat.completions.create(
    model = "deepseek-flash",
    messages = messages,
    tools = tools,
)

response_message = first_response.choices[0].message

tool_calls = response_message.tool_calls

if tool_calls:
    print(f"检测到调用len{len(tool_calls)}个本地工具！")
    messages.append(response_message)

    for tool_call in tool_calls:
        func_name = tool_call.function.name
        func_args = json.loads(tool_call.function.arguments)

        print(f"准备调用工具： {func_name}, 参数： {func_args}")

        tool_func = AVAILABLE_TOOLS.get(func_name)

        if tool_func:
            tool_output = tool_func(**func_args)
        else:
            tool_output = json.dumps(
                {"error" : f"Don't exit tool named {func_name}"}
            )

        messages.append(
            {
                "role" : "tool",
                "tool_call_id" : tool_call.id,
                "content" : str(tool_output)
            }
        )

    final_response = client.chat.completions.create(
        model = "deepseek-flash",
        messages = messages,
        stream = True
    )

    for chunk in final_response:
        delta_content = chunk.choices[0].delta.content
        if delta_content:
            print(delta_content, end="", flush=True)

else:
    print("直接回复：\n", response_message.content)
