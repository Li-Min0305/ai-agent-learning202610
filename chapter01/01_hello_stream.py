import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")
base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

client = OpenAI(api_key=api_key, base_url=base_url)

response = client.chat.completions.create(
    model = "deepseek-flash",
    messages = [
        {"role" : "system", "content" : "你是一个资深严谨的AI系统架构师"},
        {"role" : "user" , "content" : "用100字精炼概述为什么做AI Agent 必须掌握流式输出（Streaming）？"}
    ],
    stream = True
    )

for chunk in response:
    delta_content = chunk.choices[0].delta.content
    if delta_content:
        print(delta_content, end="", flush=True)