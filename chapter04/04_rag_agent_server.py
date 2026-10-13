import os
import json
from dotenv import load_dotenv
from openai import AsyncOpenAI
import chromadb
from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import  BaseModel, Field


load_dotenv()

app = FastAPI(title="星火大学 RAG 智能问答系统", version="1.0.0")

client = AsyncOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
)

chroma_client = chromadb.PersistentClient(path="./chapter04/chroma_storage/")
collection = chroma_client.get_collection(name = "campus_guide_collection")

class RAGRequest(BaseModel):
    query: str = Field(
        ...,
        description="用户的提问",
        example="奖金有多少？"
    )

async def rag_stream_generator(user_query: str):
    search_result = collection.query(query_texts=[user_query], n_results=4)
    retrieved_docs = search_result["documents"][0]

    context_str = "\n\n".join([f"【参考资料{i+1}】:\n{doc}" for i, doc in enumerate(retrieved_docs)])

    system_prompt = f"""你是一个严谨的星火大学智能校务助理。
请严格根据以下提供的【参考资料】回答用户问题。
要求：
1. 答案必须完全忠于参考资料，严禁自行编造或引入外部未经证实的信息。
2. 如果参考资料中没有提及答案，请坦诚回答：“抱歉，学校知识库中未查询到相关规定。”
3. 回答完毕后，简要注明你参考了哪个片段。
{context_str}"""

    stream = await client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ],
        stream=True
    )

    async for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            payload = json.dumps({"text": delta}, ensure_ascii=False)
            yield f"data: {payload}\n\n"

    yield "data: [DONE]\n\n"

@app.post("/api/rag/chat")
async def rag_chat(req: RAGRequest):
    return StreamingResponse(
        rag_stream_generator(req.query),
        media_type="text/event-stream"
    )

@app.get("/")
async def get_ui():
    return FileResponse("chapter03/index.html")