#敏感词过滤
import jieba
def check_sensitive_words(text, sensitive_words):
    """
    检查文本中的敏感词
    :param text: 待检查的文本
    :param sensitive_words: 敏感词列表
    :return: 敏感词统计信息
    """
    words = jieba.lcut(text)
    found_words = []
    positions = []
    for idx, word in enumerate(words):
        if word in sensitive_words:
            found_words.append(word)
            positions.append(idx)
    result = {
        "count": len(found_words),
        "words": found_words,
        "positions": positions,
        "has_sensitive": len(found_words) > 0
    }
    return result
sensitive_list = ["暴力", "赌博", "色情", "诈骗", "违法"]
text1 = "这是一个正常的文章，讲述人工智能的发展"
text2 = "这个文章包含暴力内容和赌博信息"
result1 = check_sensitive_words(text1, sensitive_list)
result2 = check_sensitive_words(text2, sensitive_list)
print("文本1检查结果:", result1)
print("文本2检查结果:", result2)
if result2["has_sensitive"]:
    print(f"发现 {result2['count']} 个敏感词：{result2['words']}")
    print(f"位置索引：{result2['positions']}")