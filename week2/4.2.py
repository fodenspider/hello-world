#文件安全读取
def safe_read_file():
    file_path = input("请输入文件路径：")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            print("\n文件读取成功！")
            print("文件内容如下：")
            print("-" * 30)
            print(content)
    except FileNotFoundError:
        print("错误：文件不存在，请检查路径是否正确！")
    except UnicodeDecodeError:
        print("错误：文件编码错误，无法使用UTF-8读取！")
safe_read_file()