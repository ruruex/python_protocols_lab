from matplotlib import pyplot as plt
import os

# Configure the font
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.family'] ='sans-serif'

def mat_line_chart(lines_list,title,x_label,y_label):
    # change canvas size
    fig = plt.figure(figsize=(6,6))

    # 表示在1×1的网格中创建第1个子图
    ax = fig.add_subplot(1,1,1)

    # set X axis time format
    import matplotlib.dates as mdate
    ax.xaxis.set_major_formatter(mdate.DateFormatter('%H:%M'))
    # set interval as 1 min
    ax.xaxis.set_major_locator(mdate.MinuteLocator(interval=1))

    # set Y axis time format
    import matplotlib.ticker as mtick
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%3.1f%%'))

    # Y axis data range
    ax.set_ylim(ymin=0,ymax=100)

    # Add title and label
    plt.title(title) 
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # self adpative
    fig.autofmt_xdate()

    # loop x_y_list, draw the line chart
    for x_list, y_list, line_style, color, line_name in lines_list:
        ax.plot(x_list, y_list, linestyle=line_style,color=color,label=line_name)

    # set legend 
    ax.legend(loc='upper left')

    # save to local
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'line_chart.png')
    plt.savefig(file_path)

    # show
    plt.show()

if __name__ == "__main__":
    from datetime import datetime, timedelta
    from random import random, choice
    
    # line number
    line_no = 2

    data_points_count = 10
    color_list = ['red','blue','green','yellow']

    now = datetime.now()

    lines_list = []
    
    # Generate multiple lines
    for line in range(line_no):

        line_name = f'line{line+1}'

        line_x_list = []
        line_y_list = []

        for d in range(data_points_count):

            line_x_list.append(now+timedelta(minutes=d))
            line_y_list.append(random()*100)

        lines_list.append([line_x_list,line_y_list,'solid',choice(color_list),line_name])

    # draw the line chart
    mat_line_chart(lines_list,'CPU利用率','时间','%')
