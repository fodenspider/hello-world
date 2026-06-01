#文本统计
def analyze_text():
    line_count = 0
    char_count = 0
    max_line_length = 0
    file_path = input("请输入文件路径：")
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line_count += 1
            line_length = len(line.strip("\n"))
            char_count += line_length
            if line_length > max_line_length:
                max_line_length = line_length
    print("文件总行数：", line_count)
    print("文件总字数：", char_count)
    print("最长行长度：", max_line_length)
analyze_text()