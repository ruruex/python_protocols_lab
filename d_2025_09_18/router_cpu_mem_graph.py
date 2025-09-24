from matplotlib import pyplot as plt
import os

from read_router_cpu_mem_db import cpu_query,memory_query

# Configure the font
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.family'] ='sans-serif'

def mat_line_chart(lines_list,title,x_label,y_label,file_name):
    # change canvas size
    fig = plt.figure(figsize=(6,6))

    # 表示在1×1的网格中创建第1个子图
    ax = fig.add_subplot(1,1,1)

    # set X axis time format
    import matplotlib.dates as mdate
    ax.xaxis.set_major_formatter(mdate.DateFormatter('%H:%M'))
    # set interval to auto adjustment 
    ax.xaxis.set_major_locator(mdate.AutoDateLocator(maxticks=12))

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
    file_path = os.path.join(script_dir, file_name)
    plt.savefig(file_path)

    # show
    plt.show()


if __name__ == "__main__":
    from datetime import datetime, timedelta
    from random import choice
    
    # line count
    line_no = 2

    # color list for random choice
    color_list = ['red','blue','green','yellow']

    # Device list
    device_ip_list = ['10.128.1.51','10.128.1.91']
    cpu_list = []
    memory_list = []
    lines_list = [] 
    lines_list_2= []

    # create the line chart for CPU
    for device in device_ip_list:
        cpu_list,time_list =  cpu_query(device)
        # print(time_list)
          
        # Generate multiple lines for cpu
        lines_list.append([time_list,cpu_list,'solid',choice(color_list),'CPU utilization'])

        # draw the line chart
        mat_line_chart(lines_list,'CPU利用率','记录时间','%','cpu_utilization.png')

     # create the line chart for memory
    for device in device_ip_list:
        memory_list,time_list =  memory_query(device)
        # print(memory_list)
          
        # Generate multiple lines for cpu
        lines_list_2.append([time_list,memory_list,'solid',choice(color_list),'Memory utilization'])

        # draw the line chart
        mat_line_chart(lines_list_2,'MEM利用率','记录时间','%','memory_utilization.png')
   
