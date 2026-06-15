#正则
import re

def extract_personal_info(text):
    """
    从文本中提取个人信息：姓名、手机号、邮箱、身份证号
    """
    
    # 1. 提取姓名（假设姓名前有"姓名："或"名字："等标记）
    name_pattern = r'(?:姓名|名字|Name)[:：]?\s*([\u4e00-\u9fa5]{2,4})'
    names = re.findall(name_pattern, text)
    
    # 2. 提取手机号（1开头，第二位3-9，后面9位数字）
    phone_pattern = r'1[3-9]\d{9}'
    phones = re.findall(phone_pattern, text)
    
    # 3. 提取邮箱
    email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    emails = re.findall(email_pattern, text)
    
    # 4. 提取身份证号（15位或18位，最后一位可能是X）
    id_pattern = r'\d{17}[\dXx]|\d{15}'
    id_cards = re.findall(id_pattern, text)
    
    # 输出结果
    print("=" * 50)
    print("信息提取结果")
    print("=" * 50)
    
    if names:
        print(f"姓名：{', '.join(names)}")
    else:
        print("姓名：未找到")
    
    if phones:
        print(f"手机号：{', '.join(phones)}")
    else:
        print("手机号：未找到")
    
    if emails:
        print(f"邮箱：{', '.join(emails)}")
    else:
        print("邮箱：未找到")
    
    if id_cards:
        # 隐藏部分数字
        masked_ids = [id_num[:6] + '*' * (len(id_num)-10) + id_num[-4:] for id_num in id_cards]
        print(f"身份证号：{', '.join(masked_ids)}")
    else:
        print("身份证号：未找到")
    
    print("=" * 50)
    
    return {
        'names': names,
        'phones': phones,
        'emails': emails,
        'id_cards': id_cards
    }

# 测试数据
test_text = """
用户信息登记表

姓名：傅
联系电话：12333434334
电子邮箱：fu@example.com
身份证号码：111111111111111111

其他信息：
- 办公电话：010-88889999
- 紧急联系：18600001111
"""

# 运行提取
result = extract_personal_info(test_text)