# 待办事项
todos = []

while True:
    print("\n===== 待办事项管理 =====")
    print("1. 添加待办事项")
    print("2. 查看所有待办")
    print("3. 标记事项为已完成")
    print("4. 退出")
    
    choice = input("请输入你的选择：")
    
    if choice == "1":
        task = input("请输入待办事项内容：")
        todos.append({"内容": task, "状态": "未完成"})
        print("已添加待办事项")
    
    elif choice == "2":
        if todos:
            print("待办事项列表：")
            for i, todo in enumerate(todos, start=1):
                print(f"{i}. [{todo['状态']}] {todo['内容']}")
        else:
            print("暂无待办事项")
    
    elif choice == "3":
        if todos:
            try:
                index = int(input("请输入要标记完成的事项编号：")) - 1
                if 0 <= index < len(todos):
                    todos[index]["状态"] = "已完成"
                    print("已标记为完成")
                else:
                    print("编号无效")
            except ValueError:
                print("请输入有效的数字")
        else:
            print("暂无待办事项")
    
    elif choice == "4":
        print("退出待办事项管理")
        break
    
    else:
        print("无效的选择，请重新输入")