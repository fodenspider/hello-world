# 文本清洗
s = input("请输入要清洗的话：")
s = s.strip()
s = " ".join(s.split())
s = s.replace("，", ",")
s = s.replace("。", ".")
s = s.replace("！", "!")
s = s.replace("？", "?")
print("清洗结果：", s)