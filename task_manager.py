# task_manager.py
import os
from datetime import datetime
from task import Task


class TaskManager:
    """任务管理器类，负责任务的增删、读取、保存、统计等管理工作."""
    def __init__(self, file_path="data.txt"):
        """
        初始化任务管理器
        :param file_path: 存储任务数据的文本文件路径，默认 data.txt
        """
        self.file_path = file_path  # 数据文件路径
        self.tasks = []              # 内存中存放所有任务对象的列表
        self.load_data()             # 实例化时自动从文件加载历史任务

    def load_data(self):
        """启动时自动读取文件，加载上次保存的任务数据到内存."""
        # 如果文件不存在，直接返回，无需读取
        if not os.path.exists(self.file_path):
            return
        try:
            # 打开文件，逐行读取任务字符串并转为Task对象
            with open(self.file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # 跳过空行
                    if line:
                        task = Task.from_string(line)
                        if task:
                            self.tasks.append(task)
        except Exception as e:
            print(f"读取数据失败: {e}")

    def save_data(self):
        """将内存中当前所有任务写入文件，持久化保存"""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                # 遍历所有任务，调用to_string转为字符串写入文件，一行一个任务
                for task in self.tasks:
                    f.write(task.to_string() + '\n')
        except Exception as e:
            print(f"保存数据失败: {e}")

    def add_task(self, title: str, priority: str, due_date: str):
        """
        添加新任务到任务列表
        :param title: 任务标题
        :param priority: 任务优先级
        :param due_date: 截止日期，格式 YYYY-MM-DD
        """
        new_task = Task(title, priority, due_date)
        self.tasks.append(new_task)

    def get_all_tasks(self):
        """获取全部任务列表"""
        return self.tasks

    def get_task_by_index(self, index: int):
        """
        根据从1开始的编号获取任务对象
        :param index: 用户看到的任务序号（从1开始）
        :return: 找到返回Task对象，找不到返回None
        """
        # 转为列表下标（列表下标从0开始）
        if 0 <= index - 1 < len(self.tasks):
            return self.tasks[index - 1]
        return None

    def delete_task(self, index: int) -> bool:
        """
        根据任务序号删除任务
        :param index: 用户看到的任务序号（从1开始）
        :return: 删除成功返回True，序号无效返回False
        """
        if 0 <= index - 1 < len(self.tasks):
            self.tasks.pop(index - 1)
            return True
        return False

    def get_overdue_tasks(self):
        """获取所有未完成且已经过期的任务列表"""
        today = datetime.now().strftime('%Y-%m-%d')
        # 筛选条件：任务未完成 + 截止日期早于今天
        return [t for t in self.tasks if not t.completed and t.due_date < today]

    def get_statistics(self):
        """
        获取任务统计信息
        :return: 字典，包含总任务数、已完成、未完成、逾期数量、完成率
        """
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t.completed)
        uncompleted = total - completed
        overdue = len(self.get_overdue_tasks())
        # 计算完成率，避免除以0报错
        rate = (completed / total * 100) if total > 0 else 0
        return {
            "total": total,
            "completed": completed,
            "uncompleted": uncompleted,
            "overdue": overdue,
            "rate": rate
        }
