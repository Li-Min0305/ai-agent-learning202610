import numpy as np
import chromadb.utils.embedding_functions as embedding_functions

def cosine_similarity(vec1, vec2):
    """
    计算两个向量之间的夹角余弦值
    值越接近1.0， 说明语义越相近；越接近 0，说明毫无关联。
    """
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)

ef = embedding_functions.DefaultEmbeddingFunction()

text1 = "今天天气晴朗，非常适合去公园散步。"
text2 = "外面的阳光很好，我想去户外走走呼吸新鲜空气。"
text3 = "基于量子纠缠的超导材料在极低温下的电阻特性分析。"

print(">>> 正在将文本转换成高维向量空间中的坐标点 (Embedding)...\n")

vectors = ef([text1, text2, text3])

vec1 = vectors[0]
vec2 = vectors[1]
vec3 = vectors[2]

print(f"句子 1 转换后的向量维度数量: {len(vec1)} 个浮点数")
print(f"句子 1 的前 5 个坐标值: {vec1[:5]}...\n")
# 3. 计算语义相似度
sim_1_and_2 = cosine_similarity(vec1, vec2)
sim_1_and_3 = cosine_similarity(vec1, vec3)


print("========================================")
print("📊 语义相似度计算结果（0.0 ~ 1.0）：")
print("========================================")
print(f"句子 1: '{text1}'")
print(f"句子 2: '{text2}'")
print(f"👉 句子 1 与 句子 2 的语义相似度: 【{sim_1_and_2:.4f}】 (极其相近！)")
print("----------------------------------------")
print(f"句子 1: '{text1}'")
print(f"句子 3: '{text3}'")
print(f"👉 句子 1 与 句子 3 的语义相似度: 【{sim_1_and_3:.4f}】 (几乎毫无关联！)")