# task_manager.py
import os
from datetime import datetime
from task import Task

class TaskManager:
    def __init__(self, file_path="data.txt"):
        self.file_path = file_path
        self.tasks = []
        self.load_data()

    def load_data(self):
        """启动时自动读取上次的数据"""
        if not os.path.exists(self.file_path):
            return
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        task = Task.from_string(line)
                        if task:
                            self.tasks.append(task)
        except Exception as e:
            print(f"读取数据失败: {e}")

    def save_data(self):
        """退出时自动保存"""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                for task in self.tasks:
                    f.write(task.to_string() + '\n')
        except Exception as e:
            print(f"保存数据失败: {e}")

    def add_task(self, title: str, priority: str, due_date: str):
        new_task = Task(title, priority, due_date)
        self.tasks.append(new_task)

    def get_all_tasks(self):
        return self.tasks

    def get_task_by_index(self, index: int):
        """根据从1开始的编号获取任务"""
        if 0 <= index - 1 < len(self.tasks):
            return self.tasks[index - 1]
        return None

    def delete_task(self, index: int) -> bool:
        if 0 <= index - 1 < len(self.tasks):
            self.tasks.pop(index - 1)
            return True
        return False

    def get_overdue_tasks(self):
        today = datetime.now().strftime('%Y-%m-%d')
        return [t for t in self.tasks if not t.completed and t.due_date < today]

    def get_statistics(self):
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t.completed)
        uncompleted = total - completed
        overdue = len(self.get_overdue_tasks())
        rate = (completed / total * 100) if total > 0 else 0
        return {
            "total": total,
            "completed": completed,
            "uncompleted": uncompleted,
            "overdue": overdue,
            "rate": rate
        }