#BMI
height = float(input("输入你的身高(单位米)："))
weight = float(input("输入你的体重(单位公斤)："))
bmi = weight / (height*height)
if bmi < 18.5:
    result = "偏瘦"
elif bmi < 25:
    result = "正常"
elif bmi < 28:
    result = "偏胖"
else:
    result = "肥胖"
print(f"BMI指数为{bmi:.2f},体重是{result}")