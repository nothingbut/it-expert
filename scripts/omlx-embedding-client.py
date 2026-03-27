#!/usr/bin/env python3
"""
oMLX 嵌入模型客户端示例
演示如何使用 nomic-embed-text-v2-moe 进行文本嵌入
"""

import requests
import numpy as np
from typing import List, Union
import json

class OMLXEmbeddingClient:
    """oMLX 嵌入客户端"""

    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url.rstrip('/')
        self.model = "nomic-ai/nomic-embed-text-v2-moe"

    def get_embedding(self, text: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
        """
        获取文本嵌入

        Args:
            text: 单个文本或文本列表

        Returns:
            嵌入向量或嵌入向量列表
        """
        # 确保输入是列表
        is_single = isinstance(text, str)
        texts = [text] if is_single else text

        # 调用 API
        response = requests.post(
            f"{self.base_url}/v1/embeddings",
            json={
                "model": self.model,
                "input": texts
            }
        )
        response.raise_for_status()

        # 解析结果
        data = response.json()
        embeddings = [item['embedding'] for item in data['data']]

        # 如果输入是单个文本，返回单个嵌入
        return embeddings[0] if is_single else embeddings

    def cosine_similarity(self, emb1: List[float], emb2: List[float]) -> float:
        """计算余弦相似度"""
        a = np.array(emb1)
        b = np.array(emb2)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def find_most_similar(self, query: str, candidates: List[str], top_k: int = 3) -> List[tuple]:
        """
        找到最相似的候选文本

        Args:
            query: 查询文本
            candidates: 候选文本列表
            top_k: 返回前 k 个最相似的结果

        Returns:
            [(候选文本, 相似度分数), ...]
        """
        # 获取所有嵌入
        all_texts = [query] + candidates
        embeddings = self.get_embedding(all_texts)

        # 计算相似度
        query_emb = embeddings[0]
        candidate_embs = embeddings[1:]

        similarities = [
            (candidate, self.cosine_similarity(query_emb, cand_emb))
            for candidate, cand_emb in zip(candidates, candidate_embs)
        ]

        # 排序并返回 top_k
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]

    def check_health(self) -> bool:
        """检查服务健康状态"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False

    def list_models(self) -> List[str]:
        """列出所有可用模型"""
        response = requests.get(f"{self.base_url}/v1/models")
        response.raise_for_status()
        data = response.json()
        return [model['id'] for model in data['data']]


def example_basic_embedding():
    """示例1：基本嵌入"""
    print("=" * 50)
    print("示例1：基本文本嵌入")
    print("=" * 50)

    client = OMLXEmbeddingClient()

    text = "人工智能正在改变世界"
    embedding = client.get_embedding(text)

    print(f"文本: {text}")
    print(f"嵌入维度: {len(embedding)}")
    print(f"前10个值: {embedding[:10]}")
    print()


def example_batch_embedding():
    """示例2：批量嵌入"""
    print("=" * 50)
    print("示例2：批量文本嵌入")
    print("=" * 50)

    client = OMLXEmbeddingClient()

    texts = [
        "苹果是一种水果",
        "香蕉富含钾元素",
        "Python 是一种编程语言",
        "JavaScript 用于网页开发"
    ]

    embeddings = client.get_embedding(texts)

    print(f"输入文本数量: {len(texts)}")
    print(f"输出嵌入数量: {len(embeddings)}")
    print(f"每个嵌入维度: {len(embeddings[0])}")
    print()


def example_semantic_search():
    """示例3：语义搜索"""
    print("=" * 50)
    print("示例3：语义搜索")
    print("=" * 50)

    client = OMLXEmbeddingClient()

    # 知识库
    documents = [
        "苹果公司发布了新款 iPhone",
        "机器学习是人工智能的一个分支",
        "Python 是最流行的编程语言之一",
        "深度学习在图像识别中表现出色",
        "苹果派是一种美味的甜点",
        "TensorFlow 是 Google 开发的机器学习框架",
    ]

    # 查询
    query = "人工智能技术"

    print(f"查询: {query}")
    print(f"知识库大小: {len(documents)}")
    print()

    # 搜索
    results = client.find_most_similar(query, documents, top_k=3)

    print("最相关的文档：")
    for i, (doc, score) in enumerate(results, 1):
        print(f"{i}. [{score:.4f}] {doc}")
    print()


def example_similarity_matrix():
    """示例4：相似度矩阵"""
    print("=" * 50)
    print("示例4：文本相似度矩阵")
    print("=" * 50)

    client = OMLXEmbeddingClient()

    texts = [
        "人工智能",
        "机器学习",
        "深度学习",
        "苹果水果",
    ]

    # 获取所有嵌入
    embeddings = client.get_embedding(texts)

    # 计算相似度矩阵
    n = len(texts)
    print("相似度矩阵:")
    print(" " * 15 + "  ".join([f"文本{i+1}" for i in range(n)]))

    for i in range(n):
        row = [f"{texts[i][:10]:12}"]
        for j in range(n):
            sim = client.cosine_similarity(embeddings[i], embeddings[j])
            row.append(f"{sim:.4f}")
        print("  ".join(row))
    print()


def example_clustering():
    """示例5：文本聚类"""
    print("=" * 50)
    print("示例5：简单文本聚类")
    print("=" * 50)

    client = OMLXEmbeddingClient()

    texts = [
        # 科技类
        "人工智能正在改变世界",
        "机器学习算法越来越先进",
        "深度学习在图像识别中应用广泛",
        # 水果类
        "苹果是一种营养丰富的水果",
        "香蕉含有丰富的维生素",
        "橙子富含维生素C",
        # 编程类
        "Python 是最流行的编程语言",
        "JavaScript 用于网页开发",
        "Rust 是一种系统编程语言",
    ]

    # 获取嵌入
    embeddings = client.get_embedding(texts)

    # 简单聚类：找到与第一个文本最相似的
    print("以 '人工智能正在改变世界' 为中心的相似文本：")
    similarities = [
        (text, client.cosine_similarity(embeddings[0], emb))
        for text, emb in zip(texts, embeddings)
    ]
    similarities.sort(key=lambda x: x[1], reverse=True)

    for text, score in similarities[:4]:
        print(f"  [{score:.4f}] {text}")
    print()


def main():
    """主函数"""
    print("\n" + "=" * 50)
    print("oMLX 嵌入模型客户端示例")
    print("模型: nomic-ai/nomic-embed-text-v2-moe")
    print("=" * 50 + "\n")

    # 检查服务状态
    client = OMLXEmbeddingClient()
    if not client.check_health():
        print("❌ 错误：无法连接到 oMLX 服务")
        print("请确保 oMLX 服务正在运行：")
        print("  cd ~/omlx && python -m omlx.server")
        return

    print("✅ oMLX 服务运行中\n")

    # 列出可用模型
    try:
        models = client.list_models()
        print(f"可用模型: {', '.join(models)}\n")
    except:
        print("⚠️  无法获取模型列表\n")

    # 运行示例
    try:
        example_basic_embedding()
        example_batch_embedding()
        example_semantic_search()
        example_similarity_matrix()
        example_clustering()

        print("=" * 50)
        print("✅ 所有示例运行完成")
        print("=" * 50)

    except Exception as e:
        print(f"❌ 错误: {e}")
        print("\n可能的原因：")
        print("1. 模型未加载，请运行：")
        print("   bash omlx-add-embedding-model.sh")
        print("2. oMLX 服务未启动")
        print("3. 网络连接问题")


if __name__ == "__main__":
    main()
