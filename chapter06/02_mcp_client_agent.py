import os
import json
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"),base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"))

async def main():
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "chapter06/01_mcp_server.py"]
    )

    print("正在连接 01 号 MCP 工具箱...")

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("Connecting Sucesses!")

            mcp_tools_resp = await session.list_tools()
            available_tools = mcp_tools_resp.tools

            openai_tools = [
                {
                    "type": "function",
                    "function": {
                        "name": t.name,
                        "description": t.description,
                        "parameters": t.inputSchema
                    }
                }
                for t in available_tools
            ]

            user_prompt = "请查一下小李的成绩，并看看服务器磁盘剩余空间。"
            messages = [{"role": "user", "content": user_prompt}]
            response = await client.chat.completions.create(
                model="deepseek-flash",
                messages=messages,
                tools=openai_tools
            )

            response_msg = response.choices[0].message
            tool_calls = response_msg.tool_calls

            if tool_calls:
                messages.append(response_msg)

                for tc in tool_calls:
                    func_name = tc.function.name
                    func_args = json.loads(tc.function.arguments)

                    print(f"准备调用工具: {func_name}，参数: {func_args}")

                    tool_result = await session.call_tool(func_name, func_args)
                    result_text = "\n".join([c.text for c in tool_result.content if hasattr(c, "text")])

                    messages.append(
                        {"role": "tool","tool_call_id": tc.id, "content": result_text}
                    )

                final_res = await client.chat.completions.create(
                    model="deepseek-flash",
                    messages=messages
                )
                print("\nAI 最终回复:", final_res.choices[0].message.content)


if __name__ == "__main__":
    asyncio.run(main())