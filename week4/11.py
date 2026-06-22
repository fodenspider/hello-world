#练习1，数据清洗
scores = [85, 92, None, 78, 96, 88, 92, None]
filtered = [s for s in scores if s is not None]  # [85,92,78,96,88,92]
unique_scores = list(dict.fromkeys(filtered))  # [85,92,78,96,88]
avg = sum(unique_scores) / len(unique_scores)
print(f"清洗后平均分：{avg:.2f}")