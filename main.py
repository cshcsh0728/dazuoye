# main.py
import sys
import datetime
from task_manager import TaskManager
from report_generator import generate_html_report
from chart_generator import generate_chart


def get_valid_date_input(prompt: str) -> str:
    """验证日期格式 YYYY-MM-DD"""
    while True:
        date_str = input(prompt).strip()
        try:
            datetime.datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except ValueError:
            print("日期格式错误，请重新输入（格式如：2026-10-08）：")


def get_valid_int_input(prompt: str, max_val: int = None) -> int:
    """验证整数输入，处理字母、超大数字、回车"""
    while True:
        try:
            val = input(prompt).strip()
            if not val:
                raise ValueError("输入不能为空")
            num = int(val)
            if max_val is not None and (num < 1 or num > max_val):
                print(f"编号超出范围，请输入 1 到 {max_val} 之间的数字。")
                continue
            return num
        except ValueError:
            print("输入无效，请输入有效的数字：")


def main():
    manager = TaskManager()

    while True:
        print("\n" + "=" * 30)
        print("      任务清单管理系统")
        print("=" * 30)
        print("1. 添加任务")
        print("2. 查看全部")
        print("3. 标记完成")
        print("4. 删除任务")
        print("5. 搜索与筛选")
        print("6. 统计")
        print("7. 导出报告 (HTML)")
        print("8. 生成图表 (PNG)")
        print("9. 保存并退出")
        print("=" * 30)

        choice = input("请选择操作 (1-9): ").strip()

        if choice == '1':
            title = input("请输入任务标题：").strip()
            if not title:
                print("标题不能为空！")
                continue
            priority = ""
            while priority not in ["高", "中", "低"]:
                priority = input("请输入优先级 (高/中/低)：").strip()
                if priority not in ["高", "中", "低"]:
                    print("优先级只能是 高、中、低 其中之一！")
            due_date = get_valid_date_input("请输入截止日期 (格式 YYYY-MM-DD，如 2026-10-08)：")
            manager.add_task(title, priority, due_date)
            print("任务添加成功！")

        elif choice == '2':
            tasks = manager.get_all_tasks()
            if not tasks:
                print("当前清单为空，请先添加任务。")
            else:
                print("-" * 60)
                print(f"{'编号':<5}{'优先级':<8}{'截止日期':<15}{'状态':<10}{'标题'}")
                print("-" * 60)
                today = datetime.datetime.now().strftime('%Y-%m-%d')
                for i, task in enumerate(tasks, 1):
                    status = "已完成" if task.completed else "未完成"
                    # 逾期判断
                    is_overdue = not task.completed and task.due_date < today
                    flag = "[逾期]" if is_overdue else ""
                    print(f"{i:<5}{task.priority:<8}{task.due_date:<15}{status:<10}{task.title} {flag}")
                print("-" * 60)

        elif choice == '3':
            tasks = manager.get_all_tasks()
            if not tasks:
                print("当前清单为空。")
                continue
            # 强制使用“查看全部”的编号
            print("请根据'查看全部'中的编号进行操作。")
            for i, task in enumerate(tasks, 1):
                print(f"{i}. {task.title}")
            idx = get_valid_int_input("请输入要标记完成的编号：", len(tasks))
            task = manager.get_task_by_index(idx)
            if task:
                if task.completed:
                    print("该任务已经是已完成状态。")
                else:
                    task.completed = True
                    print(f"任务 '{task.title}' 已标记为完成。")

        elif choice == '4':
            tasks = manager.get_all_tasks()
            if not tasks:
                print("当前清单为空。")
                continue
            # 强制使用“查看全部”的编号
            print("请根据'查看全部'中的编号进行操作。")
            for i, task in enumerate(tasks, 1):
                print(f"{i}. {task.title}")
            idx = get_valid_int_input("请输入要删除的编号：", len(tasks))
            task = manager.get_task_by_index(idx)
            if task:
                confirm = input(f"确定要删除任务 '{task.title}' 吗？(y/n): ").strip().lower()
                if confirm == 'y':
                    manager.delete_task(idx)
                    print("任务已删除。")
                else:
                    print("已取消删除。")

        elif choice == '5':
            print("\n--- 筛选与排序 ---")
            print("1. 只看未完成")
            print("2. 只看已完成")
            print("3. 只看已逾期")
            print("4. 按关键字搜索")
            print("5. 按优先级排序查看")
            print("6. 按截止日期排序查看")
            sub_choice = input("请选择：").strip()


            display_list = []
            if sub_choice == '1':
                display_list = [t for t in manager.get_all_tasks() if not t.completed]
            elif sub_choice == '2':
                display_list = [t for t in manager.get_all_tasks() if t.completed]
            elif sub_choice == '3':
                display_list = manager.get_overdue_tasks()
            elif sub_choice == '4':
                kw = input("请输入关键字：").strip()
                display_list = [t for t in manager.get_all_tasks() if kw in t.title]
            elif sub_choice == '5':
                # 优先级排序：高 -> 中 -> 低
                priority_order = {"高": 1, "中": 2, "低": 3}
                display_list = sorted(manager.get_all_tasks(), key=lambda t: priority_order.get(t.priority, 4))
            elif sub_choice == '6':
                display_list = sorted(manager.get_all_tasks(), key=lambda t: t.due_date)

            if not display_list:
                print("未找到符合条件的任务。")
            else:
                print("-" * 60)
                print(f"{'优先级':<8}{'截止日期':<15}{'状态':<10}{'标题'}")
                print("-" * 60)
                for task in display_list:
                    status = "已完成" if task.completed else "未完成"
                    print(f"{task.priority:<8}{task.due_date:<15}{status:<10}{task.title}")
                print("-" * 60)
                print("* 提示：此处结果仅供查看，标记完成或删除请回到主菜单使用查看全部中的编号。")

        elif choice == '6':
            stats = manager.get_statistics()
            print("\n--- 任务统计 ---")
            print(f"任务总数：{stats['total']}")
            print(f"已完成数：{stats['completed']}")
            print(f"未完成数：{stats['uncompleted']}")
            print(f"已逾期数：{stats['overdue']}")
            print(f"完成率  ：{stats['rate']:.2f}%")

        elif choice == '7':
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            filename = f"report_{today}.html"
            generate_html_report(manager, filename)

        elif choice == '8':
            generate_chart(manager, "chart.png")

        elif choice == '9':
            manager.save_data()
            print("数据已保存，感谢使用，再见！")
            sys.exit(0)
        else:
            print("无效的选择，请重新输入。")

if __name__ == "__main__":
    main()