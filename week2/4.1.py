#安全计算器
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "error"
    return a / b

print("简易计算器")
print("1： 加法")
print("2： 减法")
print("3： 乘法")
print("4： 除法")

# 异常处理开始
try:
    # 获取用户输入
    choice = input("请选择运算类型（1/2/3/4）：")
    num1 = int(input("请输入第一个数字："))
    num2 = int(input("请输入第二个数字："))

    # 根据选择调用不同函数
    if choice == "1":
        result = add(num1, num2)
    elif choice == "2":
        result = subtract(num1, num2)
    elif choice == "3":
        result = multiply(num1, num2)
    elif choice == "4":
        result = divide(num1, num2)
    else:
        result = "输入的运算类型无效"

    # 输出结果
    print(f"计算结果：{result}")

# 处理输入不是数字的情况
except ValueError:
    print("输入错误：请输入有效的整数！")

# 处理其他未知错误
except Exception as e:
    print(f"程序出错：{e}")