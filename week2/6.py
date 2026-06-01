#综合：记账本
import json
from datetime import datetime

FILE = "records.json"
def load_data():
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_record():
    date = input("日期（如2025-06-01，回车默认今天）：") or datetime.now().strftime("%Y-%m-%d")

    while True:
        category = input("类别：").strip()
        if category:
            break
        print("类别不能为空！")

    while True:
        try:
            amount = float(input("金额："))
            break
        except ValueError:
            print("金额必须是数字！")

    note = input("备注：")
    record = {"date": date, "category": category, "amount": amount, "note": note}

    data = load_data()
    data.append(record)
    save_data(data)
    print("添加成功！")

def show_records():
    data = load_data()
    if not data:
        print("暂无记录")
        return
    print(f"{'日期':<12}{'类别':<8}{'金额':<8}{'备注'}")
    print("-"*40)
    for r in data:
        print(f"{r['date']:<12}{r['category']:<8}{r['amount']:<8.2f}{r['note']}")

def stats_by_category():
    data = load_data()
    if not data:
        print("暂无记录")
        return
    stats = {}
    for r in data:
        stats[r["category"]] = stats.get(r["category"], 0) + r["amount"]
    print(f"{'类别':<8}{'总金额':<10}")
    print("-"*18)
    for cat, total in stats.items():
        print(f"{cat:<8}{total:<10.2f}")

def main():
    while True:
        print("\n1.添加 2.查看 3.统计 4.退出")
        choice = input("选择：")
        if choice == "1":
            add_record()
        elif choice == "2":
            show_records()
        elif choice == "3":
            stats_by_category()
        elif choice == "4":
            break

if __name__ == "__main__":
    main()