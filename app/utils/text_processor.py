import re


class TextProcessor:
    @staticmethod
    def clean_text(text: str) -> str:
        """清洗文本：去除多余空格，保留中文标点"""
        # 只去掉特殊符号，保留中文、英文、数字、常见标点
        text = re.sub(r'[^\w\s\u4e00-\u9fff.,;:!?\-，。；：！？、]', '', text)
        # 多个空格合并为一个
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    @staticmethod
    def split_chunks(text: str, chunk_size: int = 200, overlap: int = 50) -> list[str]:
        """按字符分块，带重叠防止断句"""
        chunks = []
        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            start += (chunk_size - overlap)
        return chunks