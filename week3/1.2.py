#银行存款类
class BankAccount:
    def __init__(self, account_holder, balance=0):
        self.account_holder = account_holder
        self.balance = balance
    
    def deposit(self, amount):
        """存款"""
        if amount > 0:
            self.balance += amount
            return f"存款成功！当前余额：{self.balance}元"
        return "存款金额必须大于0"
    
    def withdraw(self, amount):
        """取款"""
        if amount <= 0:
            return "取款金额必须大于0"
        elif amount > self.balance:
            return f"余额不足！当前余额：{self.balance}元，尝试取款：{amount}元"
        else:
            self.balance -= amount
            return f"取款成功！当前余额：{self.balance}元"
    
    def check_balance(self):
        """查询余额"""
        return f"{self.account_holder}的余额：{self.balance}元"

# 测试
account = BankAccount("李四", 1000)
print(account.check_balance())      # 李四的余额：1000元
print(account.deposit(500))         # 存款成功！当前余额：1500元
print(account.withdraw(200))        # 取款成功！当前余额：1300元
print(account.withdraw(2000))       # 余额不足！当前余额：1300元，尝试取款：2000元