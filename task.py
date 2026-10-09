
import re
from datetime import datetime


class Task:
    """单个待办任务。

    一行文本格式：标题|优先级|截止日期|状态
    例如：写高数作业|高|2026-10-08|未完成
    """

    PRIORITIES = {"高", "中", "低"}
    STATUS_COMPLETED = "已完成"
    STATUS_UNCOMPLETED = "未完成"
    DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")

    def __init__(self, title: str, priority: str, due_date: str, completed: bool = False):
        self.title = title.strip()
        self.priority = priority.strip()
        self.due_date = due_date.strip()
        self.completed = bool(completed)

    @classmethod
    def is_valid_date(cls, date_str: str) -> bool:
        """严格验证 YYYY-MM-DD，且必须是真实存在的日期。"""
        if not isinstance(date_str, str) or not cls.DATE_PATTERN.match(date_str):
            return False
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    @classmethod
    def is_valid_priority(cls, priority: str) -> bool:
        return priority in cls.PRIORITIES

    def to_string(self) -> str:
        """将任务转换为规定格式的字符串：写高数作业|高|2026-10-08|未完成"""
        status = self.STATUS_COMPLETED if self.completed else self.STATUS_UNCOMPLETED
        return f"{self.title}|{self.priority}|{self.due_date}|{status}"

    @classmethod
    def from_string(cls, line: str):
        """从字符串解析为 Task 对象；格式不合法时返回 None，避免程序崩溃。"""
        if not line or not line.strip():
            return None

        # 用 rsplit 从右侧切 3 次，这样即使标题里含 | 也能正确解析
        parts = line.strip().rsplit("|", 3)
        if len(parts) != 4:
            return None

        title, priority, due_date, status = [p.strip() for p in parts]

        if not title:
            return None
        if not cls.is_valid_priority(priority):
            return None
        if not cls.is_valid_date(due_date):
            return None

        if status == cls.STATUS_COMPLETED:
            completed = True
        elif status == cls.STATUS_UNCOMPLETED:
            completed = False
        else:
            return None

        return cls(title, priority, due_date, completed)

    def __str__(self):
        status = self.STATUS_COMPLETED if self.completed else self.STATUS_UNCOMPLETED
        return f"{self.priority} | {self.due_date} | {status} | {self.title}"

    def __repr__(self):
        return (
            f"Task(title={self.title!r}, priority={self.priority!r}, "
            f"due_date={self.due_date!r}, completed={self.completed!r})"
        )

    def __eq__(self, other):
        if not isinstance(other, Task):
            return NotImplemented
        return (
            self.title == other.title
            and self.priority == other.priority
            and self.due_date == other.due_date
            and self.completed == other.completed
        )