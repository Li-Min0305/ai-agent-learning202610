import os
import chromadb

def get_chunks():
    with open("chapter04/data/campus_guide.txt", "r", encoding="utf-8") as f:
        content = f.read()

    clean = "".join([l.strip() for l in content.splitlines() if l.strip()])
    chunks, start = [], 0
    while start < len(clean):
        chunks.append(clean[start:start+120])
        start += 90

    return chunks

chunks = get_chunks()

db_path = "./chapter04/chroma_storage/"
client = chromadb.PersistentClient(path = db_path)

collection = client.get_or_create_collection(name="campus_guide_collection")

print(">>> 正在将文档块存入 ChromaDB 向量数据库并构建索引...")

collection.upsert(
    documents=chunks,
    ids=[f"chunk_{i+1}" for i in range(len(chunks))]
)

print(f"✅ 成功入库！当前知识库集合包含 【{collection.count()}】 条向量数据。\n")

user_query = "未来之星特等奖学金每年能领多少奖金？由谁来颁发证书？"
print(f"🔍 用户提问: '{user_query}'")

results = collection.query(
    query_texts=[user_query],
    n_results=2
)

print("\n========================================")
print("🎯 ChromaDB 召回的最相关文档片段：")
print("========================================")

for i, (doc, doc_id) in enumerate(zip(results["documents"][0], results["ids"][0])):
    print(f"【命中序号 {i+1}】(ID: {doc_id}):")
    print(f"{doc}\n")