#关键词
import jieba
from collections import Counter
stopwords = {
    "的", "了", "是", "在", "我", "有", "和", "就", "不", "人", 
    "都", "一", "一个", "上", "也", "很", "到", "说", "要", "去",
    "你", "会", "着", "没有", "看", "好", "自己", "这", "那", "的",
    "我们", "他们", "这些", "那些", "这个", "那个", "可以", "可能"
}

def extract_keywords(filepath, top_n=10):
    """
    提取文章关键词
    :param filepath: txt文件路径
    :param top_n: 返回前N个关键词
    :return: 关键词列表
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    words = jieba.lcut(text)
    filtered_words = [
        w for w in words 
        if w not in stopwords and len(w) >= 2 and w.strip()
    ]
    freq = Counter(filtered_words)
    top_keywords = [word for word, count in freq.most_common(top_n)]
    
    return top_keywords, freq.most_common(top_n)