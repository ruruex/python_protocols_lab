from matplotlib import pyplot as plt
import os
def mat_bing(name_list, count_list, bing_name):
    '''
    Generates and saves a pie chart using matplotlib with the given data.
    Args:
        name_list (list of str): Labels for each section of the pie chart.
        count_list (list of int or float): Values corresponding to each label, determining the size of each pie section.
        bing_name (str): Title of the pie chart.
    Notes:
        - The pie chart is saved as 'pie_chart.png' in the current working directory.
        - The function sets the font to support Chinese characters.
        - The chart is not displayed interactively (plt.show() is commented out).
    '''

    # 设置中文
    plt.rcParams['font.sans-serif'] = ['SimHei']

    # 设置图形大小，宽，高
    plt.figure(figsize=(6,6))

    # 使用count_list的比列来绘制饼状图，使用name_list作为注释
    patches,l_text, p_text = plt.pie(count_list,
                                     labels=name_list,
                                     labeldistance=1.1,
                                     autopct='%3.1f%%',
                                     shadow=False,
                                     startangle=90,
                                     pctdistance=0.6)
    
    
    # 改变文本的大小，将每一个text遍历，调用set_size方法
    for t in l_text:
        t.set_size(30)
    
    for t in p_text:
        t.set_size(30)

    # 设置x,y轴到刻度一致，这样图形是正圆
    plt.axis('equal')
    plt.title(bing_name) # 主题
    plt.legend()

    # 保存为图片
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'pie_chart.png')
    plt.savefig(file_path)

    # 显示图片
    #plt.show()

if __name__ == '__main__':
    mat_bing(['名称1','名称2','名称3'],[1000,123,444],'测试饼状图')