from matplotlib import pyplot as plt
import os


# Configure the font
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.family'] ='sans-serif'

def mat_histogram(name_list,count_list,title,x_label,y_label, color_list):
    # change canvas size
    plt.figure(figsize=(6,6))

    # horizontal histogram
    #plt.barh(name_list,count_list,height=0.5, color = color_list)
    
    # vitical histogram
    plt.bar(name_list,count_list,height=0.5, color = color_list)


    # Add title and label
    plt.title(title) 
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # save pic
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'histogram_chart.png')
    plt.savefig(file_path)


if __name__ == "__main__":
    name_list = ['name1','name2','name3','name4']
    count_list = [123,555,354,888]
    bar_name = '2025销售状况'
    x_label = '月份'
    y_label = '万'
    colors = ['red','blue','green','yellow']

    mat_histogram(name_list,count_list,bar_name,x_label,y_label, colors)    