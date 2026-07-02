import re


class TextProcessor:
    @staticmethod
    def clean_text(text: str) -> str:
        """清洗文本：去除多余空格、特殊符号"""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s\u4e00-\u9fff.,;:!?\-]', '', text)
        return text.strip()

    @staticmethod
    def split_chunks(text: str, chunk_size: int = 500, overlap: int = 100) -> list[str]:
        """按字符分块，带重叠防止断句"""
        chunks = []
        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunks.append(text[start:end])
            start += (chunk_size - overlap)
        return chunks