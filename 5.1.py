#计算器重构
def add(x,y):
    return x+y
def subtract(x,y):
    return x-y
def multiply(x,y):
    return x*y
def divide(x,y):
    if y==0:
        return "error"
    else:
        return x/y
a = float(input("输入第一个数字："))
b = float(input("输入第二个数字："))
print(f"{add(a,b)}")
print(f"{subtract(a,b)}")
print(f"{multiply(a,b)}")
print(f"{divide(a,b)}")