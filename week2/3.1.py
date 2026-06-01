#日记本
from datetime import datetime
def write():
    content = input("写日记：")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("diary.txt", "a", encoding="utf-8") as f:
        f.write(f"[{now}]\n{content}\n\n")
    print("保存日记")
write()