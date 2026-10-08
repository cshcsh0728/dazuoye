# task.py
class Task:
    def __init__(self, title: str, priority: str, due_date: str, completed: bool = False):
        self.title = title
        self.priority = priority  # 高/中/低
        self.due_date = due_date  # YYYY-MM-DD
        self.completed = completed

    def to_string(self) -> str:
        """将任务转换为规定格式的字符串：写高数作业|高|2026-10-08|未完成"""
        status = "已完成" if self.completed else "未完成"
        return f"{self.title}|{self.priority}|{self.due_date}|{status}"

    @staticmethod
    def from_string(line: str):
        """从字符串解析为 Task 对象"""
        parts = line.strip().split('|')
        if len(parts) == 4:
            title, priority, due_date, status = parts
            completed = (status == "已完成")
            return Task(title, priority, due_date, completed)
        return None

    def __str__(self):
        status = "已完成" if self.completed else "未完成"
        return f"{self.priority} | {self.due_date} | {status} | {self.title}"