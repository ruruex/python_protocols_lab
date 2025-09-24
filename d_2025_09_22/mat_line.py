# mat_line.py
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

#

def mat_line(lines_list, title, xlabel, ylabel, save_path=None):
    """
    绘制多网络接口速率-时间折线图，支持保存为PNG
    
    参数：
    lines_list: 每条线的配置列表，格式为 [时间列表, 速率列表, 线样式, 颜色, 图例标签]
    title: 图表标题
    xlabel: x轴标签
    ylabel: y轴标签
    save_path: 可选，图片保存路径（含文件名）；为None时仅显示不保存
    """
    # fix the font issue for Chinese characters
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['font.family'] ='sans-serif'

    fig, ax = plt.subplots(figsize=(10, 6))  # 创建画布

    # 遍历绘制每条折线
    for line_data in lines_list:
        time_list, speed_list, line_style, color, label = line_data
        ax.plot(time_list, speed_list, linestyle=line_style, color=color, label=label)

    # 格式化时间轴（时:分）
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    fig.autofmt_xdate()  # 自动旋转x轴标签

    # 设置图表标注
    ax.set_title(title, fontsize=14)
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.7)

    # 保存图片（若指定了save_path）
    if save_path is not None:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"图片已保存至: {save_path}")

    plt.show()  # 显示图表