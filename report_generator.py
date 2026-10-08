# report_generator.py
import datetime


def generate_html_report(manager, filename):
    stats = manager.get_statistics()
    tasks = manager.get_all_tasks()
    today = datetime.datetime.now().strftime('%Y-%m-%d')

    # 生成进度条（使用简单的块状字符或CSS样式）
    progress_bar_length = 50
    filled_length = int(progress_bar_length * stats['rate'] // 100)
    bar = '█' * filled_length + '░' * (progress_bar_length - filled_length)
    progress_bar_text = f"{bar} {stats['rate']:.1f}%"

    html_content = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>任务清单报告 - {today}</title>
        <style>
            body {{ font-family: 'Microsoft YaHei', sans-serif; margin: 20px; background-color: #f4f4f9; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
            h1 {{ text-align: center; color: #333; }}
            .stats {{ display: flex; justify-content: space-around; margin-bottom: 20px; padding: 15px; background: #eef2f5; border-radius: 5px; }}
            .stat-item {{ text-align: center; }}
            .stat-number {{ font-size: 24px; font-weight: bold; color: #007bff; }}
            .progress-container {{ margin-bottom: 20px; font-family: monospace; font-size: 18px; background: #333; color: #0f0; padding: 10px; border-radius: 5px; text-align: center;}}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background-color: #007bff; color: white; }}
            tr:hover {{ background-color: #f1f1f1; }}
            .overdue {{ color: #dc3545; font-weight: bold; }}
            .completed {{ text-decoration: line-through; color: #888; }}
            .status-uncompleted {{ color: #e67e22; }}
            .status-completed {{ color: #27ae60; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>任务清单报告</h1>
            <p style="text-align: center; color: #666;">生成日期：{today}</p>

            <div class="stats">
                <div class="stat-item"><div class="stat-number">{stats['total']}</div><div>任务总数</div></div>
                <div class="stat-item"><div class="stat-number">{stats['completed']}</div><div>已完成</div></div>
                <div class="stat-item"><div class="stat-number">{stats['uncompleted']}</div><div>未完成</div></div>
                <div class="stat-item"><div class="stat-number">{stats['overdue']}</div><div>已逾期</div></div>
            </div>

            <div class="progress-container">
                完成率：{progress_bar_text}
            </div>

            <table>
                <thead>
                    <tr>
                        <th>编号</th>
                        <th>优先级</th>
                        <th>截止日期</th>
                        <th>状态</th>
                        <th>标题</th>
                    </tr>
                </thead>
                <tbody>
    """

    for i, task in enumerate(tasks, 1):
        is_overdue = not task.completed and task.due_date < today
        row_class = 'class="overdue"' if is_overdue else ''
        title_class = 'class="completed"' if task.completed else ''
        status_class = 'class="status-completed"' if task.completed else 'class="status-uncompleted"'

        html_content += f"""
                    <tr {row_class}>
                        <td>{i}</td>
                        <td>{task.priority}</td>
                        <td>{task.due_date}</td>
                        <td {status_class}>{'已完成' if task.completed else '未完成'}</td>
                        <td {title_class}>{task.title}</td>
                    </tr>
        """

    html_content += """
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"报告已导出：{filename}")