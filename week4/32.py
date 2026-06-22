#带引用的回答
def generate_answer_with_citation(query, top_docs, llm_response=None):
    """
    生成带引用的回答
    :param query: 用户提问
    :param top_docs: 相关文档列表（来自搜索引擎）
    :param llm_response: LLM 生成的回答（可选）
    """
    print("="*60)
    print(f"用户提问：{query}")
    print("="*60)
    prompt = """请根据以下参考资料回答问题：
【参考资料】
"""
    for i, doc in enumerate(top_docs, 1):
        prompt += f"[{i}] {doc['document']}\n"
    prompt += f"""
【问题】
{query}
请基于参考资料回答，并标注引用来源。"""
    print("\n【Prompt 模板】")
    print(prompt)
    print("\n" + "="*60)
    if llm_response is None:
        llm_response = f"""根据参考资料，相关内容包括：
"""
        for i, doc in enumerate(top_docs, 1):
            llm_response += f"{i}. {doc['document']} [引用{i}]\n"
        llm_response += "\n这些内容直接回答了您的问题。"
    print("\n【LLM 回答】")
    print(llm_response)
    print("\n" + "="*60)
    print("\n【引用来源】")
    for i, doc in enumerate(top_docs, 1):
        print(f"[{i}] {doc['document']}")
        if 'overlap_words' in doc:
            print(f"    重叠词：{doc['overlap_words']}")
        print()
    
    return llm_response
def simple_search_engine(query, documents, top_k=2):
    """简易搜索引擎"""
    import jieba
    query_words = set(jieba.lcut(query))
    query_words = {w for w in query_words if len(w) >= 2}
    results = []
    for idx, doc in enumerate(documents):
        doc_words = set(jieba.lcut(doc))
        doc_words = {w for w in doc_words if len(w) >= 2}
        overlap = query_words & doc_words
        results.append({
            "index": idx,
            "document": doc,
            "overlap_count": len(overlap),
            "overlap_words": overlap
        })
    results.sort(key=lambda x: x["overlap_count"], reverse=True)
    return results[:top_k]
documents = [
    "深度学习是机器学习的一个子领域，主要研究神经网络算法。",
    "自然语言处理（NLP）让计算机理解和生成人类语言。",
    "计算机视觉（CV）使机器能够识别和理解图像内容。",
]
if __name__ == "__main__":
    query = "机器学习和神经网络"
    top_docs = simple_search_engine(query, documents, top_k=2)
    generate_answer_with_citation(query, top_docs)