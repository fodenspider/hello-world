# 多源聚合器
def get_weather(city):
    return f"【{city}】天气：晴，25℃"
def get_news(city):
    return [f"【{city}】新闻：今日科技大会召开", f"【{city}】新闻：地铁新线开通"]
def multi_source_aggregator(city):
    print(f"--- 正在查询 {city} 的信息 ---")
    weather_info = get_weather(city)
    news_list = get_news(city)
    print(weather_info)
    for news in news_list:
        print(news)
    print("-" * 30)
if __name__ == "__main__":
    multi_source_aggregator("北京")
    multi_source_aggregator("上海")