#数据分析管道
data = [
    {"name": "张三", "score": 85, "dept": "技术部"},
    {"name": "李四", "score": 50, "dept": "技术部"},
    {"name": "王五", "score": 92, "dept": "人事部"},
]
def filter_data(items):
    print("步骤1：过滤低分数据...")
    return [x for x in items if x["score"] >= 60]
def calc_stats(items):
    print("步骤2：计算平均分...")
    total_score = sum(x["score"] for x in items)
    return total_score / len(items)
def print_report(avg_score):
    print("步骤3：生成报告")
    print(f"最终结果：平均分是 {avg_score:.1f} 分")
if __name__ == "__main__":
    step1_data = filter_data(data)
    step2_result = calc_stats(step1_data)
    print_report(step2_result)