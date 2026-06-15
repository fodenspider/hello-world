import json
import os

# 创建配置文件
def create_config():
    config = {
        "window": {
            "width": 800,
            "height": 600
        },
        "theme": {
            "background": "#FFFFFF",
            "foreground": "#000000",
            "primary_color": "#007ACC"
        }
    }
    
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)
    print("配置文件创建成功！")

# 读取配置
def read_config():
    if not os.path.exists('config.json'):
        create_config()
    
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config

# 修改配置
def update_config(width=None, height=None, theme_color=None):
    config = read_config()
    
    if width:
        config['window']['width'] = width
    if height:
        config['window']['height'] = height
    if theme_color:
        config['theme']['primary_color'] = theme_color
    
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)
    print("配置更新成功！")
    
    return config

# 测试
config = read_config()
print("当前配置：", json.dumps(config, ensure_ascii=False, indent=2))

update_config(width=1920, height=1080, theme_color="#FF5733")
config = read_config()
print("更新后配置：", json.dumps(config, ensure_ascii=False, indent=2))