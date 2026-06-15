import requests
import re
import json

# ================= 练习1：工具集 =================
def search(query: str) -> dict:
    mock_db = {
        "深圳": "深圳是广东省副省级市，常住人口约1768万。",
        "人口": "中国总人口约14.1亿（2023年数据）。",
        "GDP": "2023年中国GDP总量约126万亿元人民币。"
    }
    for key, value in mock_db.items():
        if key in query:
            return {"source": "mock_search", "result": value}
    return {"source": "mock_search", "result": f"未找到关于'{query}'的信息"}

def calculator(expr: str) -> dict:
    if not re.match(r'^[\d\s\+\-\*\/\(\)\.]+$', expr):
        return {"error": "表达式包含非法字符"}
    try:
        return {"expression": expr, "result": eval(expr)}
    except Exception as e:
        return {"error": str(e)}

def get_weather(city: str) -> dict:
    try:
        url = f'https://wttr.in/{city}?format=j1'
        resp = requests.get(url, timeout=8)
        if resp.status_code == 200:
            data = resp.json()
            cur = data['current_condition'][0]
            return {
                "city": city,
                "temp_C": cur['temp_C'],
                "weather": cur['weatherDesc'][0]['value'],
                "humidity": cur['humidity']
            }
        return {"error": f"API状态码 {resp.status_code}"}
    except Exception as e:
        return {"error": f"请求失败: {e}"}

# ================= 练习2：decide_tool =================
def decide_tool(question: str) -> dict:
    if any(w in question for w in ['天气', '温度', '多少度', '气温', '下雨']):
        city = next((c for c in ['北京','上海','广州','深圳','杭州','成都'] if c in question), '深圳')
        return {"tool": "weather", "args": {"city": city}}
    
    elif any(w in question for w in ['计算', '算一下', '等于']) or \
         re.search(r'[\d]+\s*[\+\-\*\/]\s*[\d]+', question):
        match = re.search(r'[\d\s\+\-\*\/\(\)\.]+', question)
        expr = match.group(0).strip() if match else "0"
        return {"tool": "calc", "args": {"expr": expr}}
    
    else:
        return {"tool": "search", "args": {"query": question}}

# ================= 练习3：Agent Loop =================
tools = {'search': search, 'calc': calculator, 'weather': get_weather}

def agent_loop(query: str, max_steps: int = 5):
    msgs = [{'role': 'user', 'content': query}]
    for step in range(max_steps):
        print(f"\n{'='*50}\n第 {step+1} 步")
        
        decision = decide_tool(msgs[-1]['content'])
        print(f"[Think] 工具: {decision['tool']} | 参数: {decision['args']}")
        
        if decision['tool'] not in tools:
            print("无可用工具，结束循环"); break
            
        result = tools[decision['tool']](**decision['args'])
        print(f" [Act] 结果: {json.dumps(result, ensure_ascii=False)}")
        msgs.append({'role': 'tool', 'content': str(result)})
        
        if decision['tool'] in tools:
            print("一步任务完成，退出循环"); break
            
    print(f"\n 最终输出: {msgs[-1]['content']}\n{'='*50}")
    return msgs[-1]['content']

# ================= 测试入口 =================
if __name__ == "__main__":
    print("最小 Agent Loop 测试环境已启动")
    print("输入任意问题，或输入 'exit' 退出\n")
    
    while True:
        user_input = input("你: ").strip()
        if user_input.lower() in ['exit', 'quit', '退出']:
            print("再见！"); break
        if not user_input: continue
        try:
            agent_loop(user_input)
        except Exception as e:
            print(f"运行异常: {e}")