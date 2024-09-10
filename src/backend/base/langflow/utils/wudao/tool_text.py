import re
from typing import List


def clean_text(text: str) -> str:
    # 去除 HTML 标签
    text = re.sub(r'<[^>]+>', '', text)
    # 去除网页中的空白符号
    text = re.sub(r'&nbsp;', ' ', text)
    # 去除换行符和回车符
    text = re.sub(r'[\n\r]', '', text)
    # 去除乱码字符（如�、￾等不可见字符），匹配 Unicode 控制字符和特殊符号
    text = re.sub(r'[\uFFFD\uFEFF\ufffc\ufff0-\uffff]', '', text)
    # 去除乱码字符（如非中文、英文、数字、标点符号的字符）
    text = re.sub(r'[^\u4e00-\u9fff\w\s,.，。！？]', '', text)
    # 去除多余的空格
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def create_chunks(docs: List, chunk_size: int, chunk_overlap: int) -> List[str]:
    # 初始化 chunks 列表和当前索引
    chunks = []
    start_idx = 0

    while start_idx < len(docs):
        # 计算当前 chunk 的结束索引
        end_idx = start_idx + chunk_size
        # 获取当前 chunk 的字符串列表
        chunk = docs[start_idx:end_idx]
        # 将 chunk 转换为单个字符串并添加到 chunks 列表
        chunks.append(''.join(chunk))
        # 更新下一个 chunk 的开始索引
        # 确保下一个 chunk 从前一个 chunk 的末尾向前 chunk_overlap 个字符串开始
        start_idx = end_idx - chunk_overlap
    return chunks

