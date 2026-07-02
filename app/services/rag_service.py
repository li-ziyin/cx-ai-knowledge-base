import json
import os
import re
from app.utils.text_processor import TextProcessor


class RAGService:
    def __init__(self):
        self.processor = TextProcessor()
        self.chunks = []
        self.db_path = "./data/vector_db.json"
        self._load_db()

    def _load_db(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r', encoding='utf-8') as f:
                self.chunks = json.load(f).get("chunks", [])

    def _save_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump({"chunks": self.chunks}, f, ensure_ascii=False)

    def add_document(self, text: str) -> int:
        """文档入库，返回分块数量"""
        chunks = self.processor.split_chunks(text)
        self.chunks.extend(chunks)
        self._save_db()
        return len(chunks)

    def search(self, query: str, top_k: int = 3) -> list[str]:
        """关键词匹配检索"""
        if not self.chunks:
            return []

        # 提取查询关键词
        query_words = set(re.findall(r'\w+', query.lower()))
        if not query_words:
            return []

        # 给每个chunk打分
        scored = []
        for chunk in self.chunks:
            chunk_words = set(re.findall(r'\w+', chunk.lower()))
            # 计算交集数量作为相似度分数
            score = len(query_words & chunk_words)
            scored.append((score, chunk))

        # 按分数降序，取top_k
        scored.sort(key=lambda x: x[0], reverse=True)
        return [c for _, c in scored[:top_k]]


rag_service = RAGService()