#简易搜索
import jieba
documents = [
    "深度学习是机器学习的一个子领域，主要研究神经网络算法。",
    "自然语言处理（NLP）让计算机理解和生成人类语言。",
    "计算机视觉（CV）使机器能够识别和理解图像内容。",
    "强化学习通过奖励机制训练智能体做出决策。",
    "监督学习使用标注数据训练模型进行分类和预测。",
    "无监督学习从无标签数据中发现模式和结构。",
    "卷积神经网络（CNN）在图像识别任务中表现优异。",
    "循环神经网络（RNN）适合处理序列数据如文本和时间序列。",
    "Transformer架构在自然语言处理领域取得了突破性进展。",
    "生成对抗网络（GAN）可以生成逼真的图像和数据。"
]
def simple_search_engine(query, documents, top_k=2):
    """
    简易搜索引擎：基于关键词重叠度
    :param query: 用户提问
    :param documents: 文档列表
    :param top_k: 返回最相关的K个文档
    :return: 最相关的文档及重叠词
    """
    query_words = set(jieba.lcut(query))
    query_words = {w for w in query_words if len(w) >= 2}
    results = []
    for idx, doc in enumerate(documents):
        doc_words = set(jieba.lcut(doc))
        doc_words = {w for w in doc_words if len(w) >= 2}
        overlap = query_words & doc_words
        overlap_count = len(overlap)
        results.append({
            "index": idx,
            "document": doc,
            "overlap_count": overlap_count,
            "overlap_words": overlap
        })
    results.sort(key=lambda x: x["overlap_count"], reverse=True)
    return results[:top_k]
query = "机器学习 神经网络 算法"
top_docs = simple_search_engine(query, documents, top_k=2)

print(f"提问：{query}\n")
for i, result in enumerate(top_docs, 1):
    print(f"相关文档 {i}（重叠度：{result['overlap_count']}）:")
    print(f"  内容：{result['document']}")
    print(f"  重叠词：{result['overlap_words']}\n")