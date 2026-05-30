#通讯录管理
contacts = {}

while True:
    print("\n通讯录管理")
    print("1. 添加联系人")
    print("2. 查找联系人")
    print("3. 删除联系人")
    print("4. 查看所有联系人")
    print("5. 退出")
    
    choice = input("请输入你的选择：")
    
    if choice == "1":
        name = input("请输入联系人姓名：")
        phone = input("请输入联系人电话：")
        contacts[name] = phone
        print(f"已添加联系人：{name}")
    
    elif choice == "2":
        name = input("请输入要查找的姓名：")
        if name in contacts:
            print(f"{name} 的电话是：{contacts[name]}")
        else:
            print("该联系人不存在")
    
    elif choice == "3":
        name = input("请输入要删除的姓名：")
        if name in contacts:
            del contacts[name]
            print(f"已删除联系人：{name}")
        else:
            print("该联系人不存在")
    
    elif choice == "4":
        if contacts:
            print("所有联系人：")
            for name, phone in contacts.items():
                print(f"{name}: {phone}")
        else:
            print("通讯录为空")
    
    elif choice == "5":
        print("退出通讯录管理")
        break
    
    else:
        print("无效的选择，请重新输入")