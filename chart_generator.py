# chart_generator.py
import cv2
import numpy as np
import datetime

def generate_chart(manager, filename="chart.png"):
    # 统计各优先级数量
    high = sum(1 for t in manager.get_all_tasks() if t.priority == "高")
    medium = sum(1 for t in manager.get_all_tasks() if t.priority == "中")
    low = sum(1 for t in manager.get_all_tasks() if t.priority == "低")

    # 图像基本参数
    width, height = 800, 600
    img = np.ones((height, width, 3), dtype=np.uint8) * 255  # 白色背景

    # 为了防止写死，取最大值用于计算柱子高度，至少为1避免除零
    max_value = max(high, medium, low, 1)
    max_bar_height = 400  # 最高柱子占400像素

    bar_width = 100
    gap = 100
    start_x = 200
    base_y = 500

    # 定义数据
    data = [
        {"label": "High", "value": high, "color": (0, 0, 255)},    # OpenCV 颜色为 BGR (蓝色, 绿色, 红色)
        {"label": "Medium", "value": medium, "color": (0, 255, 255)}, # 黄色
        {"label": "Low", "value": low, "color": (0, 255, 0)}      # 绿色
    ]

    # 绘图
    for i, item in enumerate(data):
        x1 = start_x + i * (bar_width + gap)
        y1 = base_y - int((item["value"] / max_value) * max_bar_height)
        x2 = x1 + bar_width
        y2 = base_y

        # 1. 画矩形（柱子）
        cv2.rectangle(img, (x1, y1), (x2, y2), item["color"], -1) # -1 表示实心

        # 2. 写数字标注（在柱子上方）
        cv2.putText(img, str(item["value"]), (x1 + 30, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        # 3. 写标签（在柱子下方）
        cv2.putText(img, item["label"], (x1 + 10, base_y + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

    # 底部基准线
    cv2.line(img, (start_x - 50, base_y), (width - 50, base_y), (0, 0, 0), 2)

    # 4. 写标题和日期
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    cv2.putText(img, "Task Priority Statistics", (200, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img, f"Date: {today}", (200, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 100, 100), 2)

    # 5. 保存图片
    cv2.imwrite(filename, img)
    print(f"图表已保存为：{filename}")