import os
def chunk_text(text: str, chunk_size: int = 120, chunk_overlap: int = 30) -> list[str]:
    """
    带重叠窗口（Overlap）的纯 Python 滑动分块算法
    """

    # 清洗多余空行
    clean_text = "".join([line.strip() for line in text.splitlines() if line.strip()])

    chunks = []
    start = 0
    text_len = len(clean_text)

    while start < text_len:
        end = start + chunk_size
        chunk = clean_text[start:end]
        chunks.append(chunk)

        start += (chunk_size - chunk_overlap)

    return chunks

file_path = "chapter04/data/campus_guide.txt"

with open(file_path, "r", encoding="utf-8") as f:
    raw_content = f.read()

chunks = chunk_text(raw_content, chunk_size=120, chunk_overlap=30)

print(f">>> 原始文档总字数: {len(raw_content)} 字")
print(f">>> 分块完成，共切出 【{len(chunks)}】 个文本块 (Chunks)\n")
for i, c in enumerate(chunks):
    print(f"----------------------------------------")
    print(f"📄 Chunk {i+1} (长度 {len(c)} 字):")
    print(c)