#时间管理器
from datetime import datetime
def study_timer():
    start_time = datetime.now()
    print("学习开始时间：", start_time.strftime("%Y-%m-%d %H:%M:%S"))
    input("按回车")
    end_time = datetime.now()
    print("学习结束时间：", end_time.strftime("%Y-%m-%d %H:%M:%S"))
    duration = end_time - start_time
    print(f"本次学习时长：{duration.total_seconds() / 60:.2f} 分钟")
study_timer()