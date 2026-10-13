import os
import json
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel, Field
from openai import AsyncOpenAI

load_dotenv()

app = FastAPI(title = "AI Agent 流式后端服务", version = "1.0.0")

client = AsyncOpenAI(
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
)

class ChatRequest(BaseModel):
    prompt : str = Field(
        ...,
        description = "用户的提问文本",
        example = "用一句话解释为什么电力如此重要？"
    )

async def event_generator(user_prompt: str):
    """
    负责一边从 DeepSeek 接收 Token，一边按照 SSE 国际标准协议打包推送给前端
    """
    stream = await client.chat.completions.create(
        model = "deepseek-flash",
        messages = [
            {"role" : "system", "content" : "你是一个严谨精炼的AI助手。"},
            {"role" : "user", "content" : user_prompt}
        ],
        stream = True
    )

    async for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            payload = json.dumps({"text": delta}, ensure_ascii = False)
            yield f"data: {payload}\n\n"

    yield "data: [DONE]\n\n"

@app.post("/api/chat/stream")
async def chat_stream(req: ChatRequest):
    return StreamingResponse(
        event_generator(req.prompt),
        media_type = "text/event-stream"
    )

# 访问根目录 http://127.0.0.1:8000/ 时，直接返回这个网页
@app.get("/")
async def get_index():
    return FileResponse("chapter03/index.html")