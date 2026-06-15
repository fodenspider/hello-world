import requests
import json
import os
import re
from datetime import datetime, timedelta
from tabulate import tabulate
from typing import List, Dict, Optional

class WeatherTool:
    
    def __init__(self, cache_file='weather_cache.json'):
        self.cache_file = cache_file
        self.cache_duration = 3600  # 缓存有效期1小时（秒）
        self.cache = self._load_cache()
    
    def _load_cache(self) -> Dict:
        """加载缓存文件"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_cache(self):
        """保存缓存到JSON文件"""
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)
    
    def _is_cache_valid(self, city: str) -> bool:
        """检查缓存是否有效（1小时内）"""
        if city not in self.cache:
            return False
        
        cache_time = datetime.fromisoformat(self.cache[city]['timestamp'])
        return datetime.now() - cache_time < timedelta(seconds=self.cache_duration)
    
    def validate_city_name(self, city: str) -> bool:
        """
        功能5：正则验证城市名
        只允许中英文城市名，不允许特殊字符
        """
        # 匹配中文、英文、数字、空格和连字符
        pattern = r'^[\u4e00-\u9fa5a-zA-Z0-9\s\-]{2,30}$'
        return bool(re.match(pattern, city))
    
    def get_weather(self, city: str) -> Optional[Dict]:
        """
        功能1：基础查询
        输入城市 → 调API → 返回温度/天气/湿度
        """
        # 输入校验
        if not self.validate_city_name(city):
            print("城市名格式不正确，只支持中英文城市名")
            return None
        
        # 功能3：检查缓存
        if self._is_cache_valid(city):
            print(f"从缓存获取 {city} 的天气信息")
            return self.cache[city]['data']
        
        # 调用API
        try:
            print(f"正在查询 {city} 的天气...")
            url = f'https://wttr.in/{city}?format=j1'
            resp = requests.get(url, timeout=10)
            
            # 功能4：异常处理
            if resp.status_code == 404:
                print(f"城市 '{city}' 不存在，请检查城市名")
                return None
            elif resp.status_code == 429:
                print("请求过于频繁，请稍后再试（API限流）")
                return None
            elif resp.status_code != 200:
                print(f"请求失败，状态码：{resp.status_code}")
                return None
            
            data = resp.json()
            
            # 提取关键信息
            current = data['current_condition'][0]
            weather_info = {
                'city': city,
                'temperature': current['temp_C'],
                'feels_like': current['FeelsLikeC'],
                'weather_desc': current['weatherDesc'][0]['value'],
                'humidity': current['humidity'],
                'wind_speed': current['windspeedKmph'],
                'query_time': datetime.now().isoformat()
            }
            
            # 保存到缓存
            self.cache[city] = {
                'data': weather_info,
                'timestamp': datetime.now().isoformat()
            }
            self._save_cache()
            
            return weather_info
            
        except requests.exceptions.Timeout:
            print("请求超时，请检查网络连接")
            return None
        except requests.exceptions.RequestException as e:
            print(f"网络错误：{e}")
            return None
        except Exception as e:
            print(f"未知错误：{e}")
            return None
    
    def batch_query(self, cities: List[str]):
        """
        功能2：批量查询
        支持多城市，表格形式输出
        """
        print(f"\n📊 批量查询 {len(cities)} 个城市的天气...\n")
        
        results = []
        for city in cities:
            weather = self.get_weather(city)
            if weather:
                results.append([
                    weather['city'],
                    f"{weather['temperature']}°C",
                    f"{weather['feels_like']}°C",
                    weather['weather_desc'],
                    f"{weather['humidity']}%",
                    f"{weather['wind_speed']} km/h"
                ])
            else:
                results.append([city, "查询失败", "-", "-", "-", "-"])
        
        # 表格形式输出
        headers = ['城市', '温度', '体感温度', '天气', '湿度', '风速']
        print(tabulate(results, headers=headers, tablefmt='grid'))
        
        return results
    
    def check_clothing_advice(self, temperature: float) -> str:
        """
        功能5：温度低于10度提示"记得加衣服"
        """
        if temperature < 10:
            return "记得加衣服！天气很冷"
        elif temperature < 20:
            return "建议穿长袖，天气凉爽"
        elif temperature < 28:
            return "天气舒适，短袖即可"
        else:
            return "天气炎热，注意防暑"
    
    def display_weather(self, weather_info: Dict):
        """格式化显示天气信息"""
        if not weather_info:
            return
        
        print("\n" + "=" * 50)
        print(f"{weather_info['city']} 天气情况")
        print("=" * 50)
        print(f"温度：{weather_info['temperature']}°C")
        print(f"体感温度：{weather_info['feels_like']}°C")
        print(f"天气：{weather_info['weather_desc']}")
        print(f"湿度：{weather_info['humidity']}%")
        print(f"风速：{weather_info['wind_speed']} km/h")
        print(f"查询时间：{weather_info['query_time']}")
        print("-" * 50)
        
        # 穿衣建议
        advice = self.check_clothing_advice(float(weather_info['temperature']))
        print(f"💡 {advice}")
        print("=" * 50 + "\n")

# ==================== Agent化版本 ====================

class WeatherAgent:
    """
    Agent认知拓展：把小工具Agent化
    理解自然语言意图，自主决定调用工具
    """
    
    def __init__(self):
        self.weather_tool = WeatherTool()
        self.tools = {
            'check_weather': self._check_weather,
            'compare_weather': self._compare_weather,
            'get_advice': self._get_advice
        }
    
    def parse_intent(self, user_input: str) -> Dict:
        """
        步骤1：理解自然语言意图
        判断用户想要什么功能
        """
        user_input = user_input.lower()
        
        # 意图识别规则
        if any(word in user_input for word in ['天气', 'weather', '气温', '温度']):
            if any(word in user_input for word in ['比较', '对比', '哪个', 'vs', '和']):
                return {'action': 'compare_weather', 'confidence': 0.9}
            elif any(word in user_input for word in ['建议', '穿什么', '带伞', '衣服']):
                return {'action': 'get_advice', 'confidence': 0.9}
            else:
                return {'action': 'check_weather', 'confidence': 0.9}
        
        elif any(word in user_input for word in ['带伞', '雨伞', '下雨']):
            return {'action': 'get_advice', 'advice_type': 'umbrella', 'confidence': 0.85}
        
        elif any(word in user_input for word in ['穿什么', '衣服', '穿搭']):
            return {'action': 'get_advice', 'advice_type': 'clothing', 'confidence': 0.85}
        
        return {'action': 'unknown', 'confidence': 0.5}
    
    def extract_parameters(self, user_input: str, intent: Dict) -> Dict:
        """
        步骤2：提取参数
        从自然语言中提取城市名等信息
        """
        params = {}
        
        # 提取城市名（简单示例，实际应该用NER）
        # 匹配"XX的天气"、"XX天气"、"查XX"等模式
        city_patterns = [
            r'([北京上海广州深圳杭州成都武汉西安南京天津重庆苏州郑州长沙青岛合肥济南沈阳大连厦门宁波福州昆明哈尔滨长春南昌贵阳南宁太原石家庄呼和浩特拉萨银川西宁乌鲁木齐]+\s*(?:的)?天气)',
            r'(?:查|查询|看)\s*([北京上海广州深圳杭州成都武汉西安南京天津重庆苏州郑州长沙青岛合肥济南沈阳大连厦门宁波福州昆明哈尔滨长春南昌贵阳南宁太原石家庄呼和浩特拉萨银川西宁乌鲁木齐]+)',
            r'([A-Za-z\s]+)\s*weather',
        ]
        
        for pattern in city_patterns:
            match = re.search(pattern, user_input)
            if match:
                params['city'] = match.group(1).replace('天气', '').strip()
                break
        
        # 提取多个城市（用于比较）
        if intent['action'] == 'compare_weather':
            # 简单提取所有可能的城市
            cities = re.findall(r'([北京上海广州深圳杭州成都武汉西安南京天津]+)', user_input)
            if len(cities) >= 2:
                params['cities'] = cities[:2]
        
        return params
    
    def _check_weather(self, city: str):
        """查询天气"""
        return self.weather_tool.get_weather(city)
    
    def _compare_weather(self, cities: List[str]):
        """比较多个城市天气"""
        return self.weather_tool.batch_query(cities)
    
    def _get_advice(self, city: str, advice_type: str = 'clothing'):
        """获取建议"""
        weather = self.weather_tool.get_weather(city)
        if not weather:
            return None
        
        if advice_type == 'umbrella':
            weather_desc = weather['weather_desc'].lower()
            if 'rain' in weather_desc or '雨' in weather_desc:
                return {
                    'advice': '建议带伞，今天有雨',
                    'weather': weather
                }
            else:
                return {
                    'advice': '不需要带伞，天气晴朗',
                    'weather': weather
                }
        else:
            temp = float(weather['temperature'])
            advice = self.weather_tool.check_clothing_advice(temp)
            return {
                'advice': advice,
                'weather': weather
            }
    
    def generate_response(self, result: Dict, intent: Dict) -> str:
        """
        步骤4：组织自然语言回复
        """
        if not result:
            return "抱歉，我无法获取相关信息，请稍后再试。"
        
        if intent['action'] == 'check_weather':
            return (f"{result['city']}当前天气：{result['weather_desc']}，"
                    f"温度{result['temperature']}°C，体感{result['feels_like']}°C，"
                    f"湿度{result['humidity']}%。"
                    f"\n{self.weather_tool.check_clothing_advice(float(result['temperature']))}")
        
        elif intent['action'] == 'get_advice':
            return f"{result['advice']}\n当前天气：{result['weather']['weather_desc']}，温度{result['weather']['temperature']}°C"
        
        return str(result)
    
    def handle_request(self, user_input: str):
        """
        Agent完整处理流程
        """
        print("\n" + "=" * 60)
        print(f"用户：{user_input}")
        print("=" * 60)
        
        # 步骤1：理解意图
        intent = self.parse_intent(user_input)
        print(f"Agent识别意图：{intent['action']} (置信度：{intent['confidence']})")
        
        if intent['action'] == 'unknown':
            print("Agent：抱歉，我还没学会这个功能。我可以帮您查询天气、比较城市天气、或提供穿衣/带伞建议。")
            return
        
        # 步骤2：提取参数
        params = self.extract_parameters(user_input, intent)
        print(f"提取参数：{params}")
        
        if not params:
            print("Agent：抱歉，我没听清楚城市名，请再说一遍。")
            return
        
        # 步骤3：调用工具
        tool_func = self.tools.get(intent['action'])
        if not tool_func:
            print("Agent：抱歉，我没有这个功能。")
            return
        
        result = tool_func(**params)
        
        # 步骤4：生成回复
        response = self.generate_response(result, intent)
        print(f"Agent：{response}")
        
        return result

# ==================== 测试演示 ====================

def demo_weather_tool():
    """演示天气工具的5个功能"""
    print("\n" + "🌤️  天气查询小工具演示".center(60, "="))
    
    weather = WeatherTool()
    
    # 功能1：基础查询
    print("\n【功能1】基础查询")
    weather_info = weather.get_weather("Beijing")
    weather.display_weather(weather_info)
    
    # 功能2：批量查询
    print("\n【功能2】批量查询")
    weather.batch_query(["Shanghai", "Guangzhou", "Shenzhen"])
    
    # 功能3：缓存测试（第二次查询会使用缓存）
    print("\n【功能3】缓存测试")
    weather.get_weather("Beijing")
    
    # 功能4：异常处理
    print("\n【功能4】异常处理")
    weather.get_weather("InvalidCity123")  # 无效城市
    weather.get_weather("")  # 空城市名
    
    # 功能5：输入校验和穿衣建议
    print("\n【功能5】输入校验和穿衣建议")
    weather.get_weather("哈尔滨")  # 低温城市

def demo_agent():
    """演示Agent化版本"""
    print("\n" + "Agent化天气助手演示".center(60, "="))
    
    agent = WeatherAgent()
    
    # 测试各种自然语言输入
    test_inputs = [
        "北京天气",
        "上海今天天气怎么样",
        "广州和深圳的天气对比一下",
        "杭州今天下雨吗？需要带伞吗？",
        "哈尔滨天气，我应该穿什么？",
        "成都天气",
    ]
    
    for user_input in test_inputs:
        agent.handle_request(user_input)

# 运行演示
if __name__ == "__main__":
    # 演示基础工具
    demo_weather_tool()
    
    # 演示Agent版本
    demo_agent()
    
    # 交互式查询
    print("\n" + "🎮 交互式天气查询（输入 'exit' 退出）".center(60, "="))
    agent = WeatherAgent()
    
    while True:
        try:
            user_input = input("\n👤 请输入：").strip()
            if user_input.lower() in ['exit', 'quit', '退出']:
                print("👋 再见！")
                break
            
            if user_input:
                agent.handle_request(user_input)
        except KeyboardInterrupt:
            print("\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 错误：{e}")