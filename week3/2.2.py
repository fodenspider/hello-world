import json

# 创建学生数据
students_data = {
    "students": [
        {"name": "张三", "scores": {"math": 90, "english": 85, "chinese": 88}},
        {"name": "李四", "scores": {"math": 78, "english": 92, "chinese": 85}},
        {"name": "王五", "scores": {"math": 95, "english": 88, "chinese": 92}},
        {"name": "赵六", "scores": {"math": 82, "english": 79, "chinese": 85}}
    ]
}

# 保存JSON文件
with open('students.json', 'w', encoding='utf-8') as f:
    json.dump(students_data, f, ensure_ascii=False, indent=4)

# 读取并解析JSON
with open('students.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 计算每个学生的平均分
students_with_avg = []
for student in data['students']:
    scores = student['scores'].values()
    avg_score = sum(scores) / len(scores)
    students_with_avg.append({
        "name": student['name'],
        "average": round(avg_score, 2),
        "scores": student['scores']
    })

# 按平均分排序（从高到低）
sorted_students = sorted(students_with_avg, key=lambda x: x['average'], reverse=True)

print("学生成绩排名：")
print("-" * 40)
for i, student in enumerate(sorted_students, 1):
    print(f"{i}. {student['name']} - 平均分: {student['average']}")
    print(f"   各科成绩: {student['scores']}")

# 计算总体平均分
all_avg = sum(s['average'] for s in sorted_students) / len(sorted_students)
print("-" * 40)
print(f"班级总体平均分: {round(all_avg, 2)}")