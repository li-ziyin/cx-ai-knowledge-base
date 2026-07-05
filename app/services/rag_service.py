import os

os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

import json
import numpy as np
from sentence_transformers import SentenceTransformer
from app.utils.text_processor import TextProcessor


class RAGService:
    def __init__(self):
        self.processor = TextProcessor()
        self.chunks = []
        self.embeddings = []
        self.db_path = "./data/vector_db.json"

        # 加载轻量级多语言模型
        print("正在加载向量模型，请稍候...")
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        print("模型加载完成！")

        self._load_db()

    def _load_db(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.chunks = data.get("chunks", [])
                self.embeddings = [np.array(e) for e in data.get("embeddings", [])]

    def _save_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump({
                "chunks": self.chunks,
                "embeddings": [e.tolist() for e in self.embeddings]
            }, f, ensure_ascii=False)

    def _get_embedding(self, text: str) -> np.ndarray:
        """获取文本嵌入向量"""
        return self.model.encode(text, convert_to_numpy=True)

    def add_document(self, text: str) -> int:
        """文档入库，返回分块数量"""
        chunks = self.processor.split_chunks(text)
        if not chunks:
            return 0

        # 获取每个片段的嵌入向量
        for chunk in chunks:
            embedding = self._get_embedding(chunk)
            self.chunks.append(chunk)
            self.embeddings.append(embedding)

        self._save_db()
        return len(chunks)

    def search(self, query: str, top_k: int = 3) -> list[str]:
        """语义检索 - 基于 sentence-transformers"""
        if not self.chunks or not self.embeddings:
            return []

        # 获取查询的嵌入向量
        query_embedding = self._get_embedding(query)

        # 计算余弦相似度
        embeddings = np.array(self.embeddings)
        query_norm = query_embedding / np.linalg.norm(query_embedding)
        emb_norms = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        similarities = np.dot(emb_norms, query_norm)

        # 获取top_k
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        return [self.chunks[idx] for idx in top_indices]


rag_service = RAGService()