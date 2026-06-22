#学生排名
#例子学生数据，按照总分降序找前5名
students = [
    {"name": "张三", "math": 85, "english": 90, "chinese": 88},
    {"name": "李四", "math": 92, "english": 88, "chinese": 95},
    {"name": "王五", "math": 78, "english": 95, "chinese": 90},
    {"name": "赵六", "math": 96, "english": 85, "chinese": 92},
    {"name": "孙七", "math": 88, "english": 92, "chinese": 85},
    {"name": "周八", "math": 90, "english": 89, "chinese": 91},
]
sorted_students = sorted(
    students, 
    key=lambda x: x["math"] + x["english"] + x["chinese"], 
    reverse=True
)
top5 = sorted_students[:5]
for stu in top5:
    total = stu["math"] + stu["english"] + stu["chinese"]
    print(f"{stu['name']}：总分 {total}")