#练习1
class Student:
    def __init__(self, name, sge, grade):
        self.name = name
        self.sge = sge
        self.grade = grade

    def introduce(self):
        return f"我是{self.name}，今年{self.sge}岁，成绩是{self.grade}"
    
S1 = Student("xiaofu",20,99)
print(S1.introduce())