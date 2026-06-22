import jieba
from collections import Counter
import os
class PersonalKnowledgeAssistant:
    def __init__(self):
        self.chunks = []
        self.index = {}
        self.chunk_id_counter = 0
    def add_note(self, title, content):
        print(f"\n📥 正在导入笔记：《{title}》...")
        paragraphs = content.split('\n\n')
        for p in paragraphs:
            if not p.strip(): continue
            chunk = {
                'id': self.chunk_id_counter,
                'content': p.strip(),
                'source': title
            }
            self.chunks.append(chunk)
            self._build_index_for_chunk(chunk['id'], p)
            self.chunk_id_counter += 1
        print(f"✅ 导入成功！共切分 {len(paragraphs)} 个段落。")
    def _build_index_for_chunk(self, cid, text):
        words = jieba.lcut(text)
        for word in words:
            if len(word) < 2: continue
            if word not in self.index:
                self.index[word] = []
            self.index[word].append(cid)
    def ask(self, query):
        print(f"\n🤖 正在思考：{query} ...")
        query_words = jieba.lcut(query)
        scores = Counter()
        for word in query_words:
            if word in self.index:
                for cid in self.index[word]:
                    scores[cid] += 1
        top_ids = [cid for cid, score in scores.most_common(2)]
        if not top_ids:
            print("❌ 没找到相关知识，请尝试其他关键词。")
            return
        print("\n📚 参考资料:")
        context_parts = []
        for cid in top_ids:
            chunk = next(c for c in self.chunks if c['id'] == cid)
            print(f"  - [来自《{chunk['source']}》]: {chunk['content'][:50]}...")
            context_parts.append(chunk['content'])
        print("\n💡 回答:")
        print(f"根据资料（{', '.join([next(c for c in self.chunks if c['id']==i)['source'] for i in top_ids])}）：")
        print("相关内容如下：")
        for part in context_parts:
            print(f"  > {part}")
    def list_notes(self):
        sources = set(c['source'] for c in self.chunks)
        print(f"\n📚 当前共有 {len(sources)} 篇笔记:")
        for s in sources:
            count = sum(1 for c in self.chunks if c['source'] == s)
            print(f"  - 《{s}》 ({count}段)")
    def delete_note(self, title):
        original_count = len(self.chunks)
        self.chunks = [c for c in self.chunks if c['source'] != title]
        removed_count = original_count - len(self.chunks)
        if removed_count > 0:
            self._rebuild_index()
            print(f"🗑️ 已删除笔记《{title}》。")
        else:
            print(f"⚠️ 未找到笔记《{title}》。")
    def _rebuild_index(self):
        self.index = {}
        for chunk in self.chunks:
            self._build_index_for_chunk(chunk['id'], chunk['content'])
    def run(self):
        print("="*40)
        print("🎓 个人知识助手 (RAG 简易版)")
        print("="*40)
        print("命令: load(导入), ask(提问), list(列出), del(删除), q(退出), ?(帮助)")
        while True:
            cmd = input("\n👉 请输入命令: ").strip()
            if cmd == 'q':
                print("👋 再见！")
                break
            elif cmd == '?':
                print("   load <标题> <内容>  : 导入笔记")
                print("   ask <问题>          : 提问")
                print("   list                : 列出笔记")
                print("   del <标题>          : 删除笔记")
            elif cmd.startswith('load'):
                parts = cmd.split(' ', 2)
                if len(parts) < 3:
                    print("❌ 格式错误: load <标题> <内容>")
                else:
                    self.add_note(parts[1], parts[2])
            elif cmd.startswith('ask'):
                query = cmd[4:]
                if query:
                    self.ask(query)
                else:
                    print("❌ 请输入问题，例如: ask 什么是 Python")
            elif cmd == 'list':
                self.list_notes()
                
            elif cmd.startswith('del'):
                title = cmd[4:]
                if title:
                    self.delete_note(title)
                else:
                    print("❌ 格式错误: del <标题>")
            else:
                print("❌ 未知命令，输入 ? 查看帮助")
if __name__ == "__main__":
    assistant = PersonalKnowledgeAssistant()
    demo_content_1 = """
    Python 是一种高级编程语言。
    Python 语法简洁清晰，非常适合初学者。
    Python 在人工智能领域应用广泛。
    """
    demo_content_2 = """
    RAG 是检索增强生成技术。
    RAG 可以让大模型使用外部知识库。
    RAG 的流程包括切分、索引、检索。
    """
    assistant.add_note("Python简介", demo_content_1)
    assistant.add_note("RAG技术", demo_content_2)
    assistant.run()