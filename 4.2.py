#猜数字
import random
num = random.randint(1,1000)
print("猜数字，范围为1到1000")
jishu = 0
while True:
    guess = int(input("输入猜测测的数字："))
    jishu +=1
    if guess < num:
        print("猜小了，继续猜")
    elif guess > num:
        print("猜大了，继续猜")
    else:
        print("猜对了")
        print(f"你一共猜了{jishu}次")
        break