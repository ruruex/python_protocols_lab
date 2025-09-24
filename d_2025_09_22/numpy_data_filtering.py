#!/usr/bin/env python3
# -*- coding=utf-8 -*-

# pip3 install numpy
from sqlalchemy.orm import sessionmaker
from create_int_monitor_db import InterfaceMonitor, engine
import numpy as np
from mat_line import mat_line

from random import choice
from pprint import pprint
from datetime import datetime, timedelta
import os,sys

# 获取当前脚本所在目录的绝对路径（d_2025_09_22）
current_script_dir = os.path.dirname(os.path.abspath(__file__))
# 计算 python_protocol 目录的绝对路径（当前目录的父目录）
python_protocol_dir = os.path.dirname(current_script_dir) 
# 将父目录添加到 sys.path
if python_protocol_dir not in sys.path:
    sys.path.append(python_protocol_dir)

Session = sessionmaker(bind=engine)
session = Session()

# 过滤10分钟以内的数据
now = datetime.now()
ten_mins_before = now - timedelta(minutes=10)

# 线的颜色列表，随机选择
color_list = ['red', 'blue', 'green', 'yellow']

# 线的类型列表，随机选择
line_style_list = ["solid", "dashed"]

# 找到唯一的device_ip和interface_name的组合
router_if_infos = session.query(InterfaceMonitor.device_ip,
                                InterfaceMonitor.interface_name).group_by(InterfaceMonitor.device_ip,
                                                                           InterfaceMonitor.interface_name).all()
print(f"router_if_infos is {router_if_infos}")
# [('10.1.1.1', 'GigabitEthernet1'), ('10.1.1.2', 'GigabitEthernet1')]

# 入向接口速率列表
in_speed_lines_list = []

# 出向接口速率列表
out_speed_lines_list = []

# 对循环进行计数
count = 0

for device_ip, interface_name in router_if_infos:
    # 过滤最近一个小时，特定device_ip与interface_name组合的全部记录数据
    device_if_info = session.query(InterfaceMonitor).\
        filter(InterfaceMonitor.device_ip == device_ip,
               InterfaceMonitor.interface_name == interface_name).\
        filter(InterfaceMonitor.record_datetime >= ten_mins_before)

    # 保存入向字节数的列表
    in_bytes_list = []
    # 保存出向字节数的列表
    out_bytes_list = []
    # 保存记录时间的列表
    record_time_list = []

    # 从过滤出来的数据库条目中，提取数据并添加到3个列表中
    for device_if in device_if_info:
        in_bytes_list.append(device_if.in_bytes)
        out_bytes_list.append(device_if.out_bytes)
        record_time_list.append(device_if.record_datetime)

    # print(in_bytes_list)
    # print(out_bytes_list)
    # print(record_time_list)

    # ---------------------使用Numpy计算字节的增量---------------------
    # numpy的diff计算列表的差值
    # np.diff([x for x in range(5)])
    # array([1, 1, 1, 1])
    # 通过这种方式获取两次获取的字节数的差值
    diff_in_bytes_list = list(np.diff(in_bytes_list))
    diff_out_bytes_list = list(np.diff(out_bytes_list))

    # ---------------------使用Numpy计算时间的增量(秒)---------------------
    # 计算两次时间对象的秒数的差值，np的多态太牛逼了
    diff_record_time_list = [x.seconds for x in np.diff(record_time_list)]

    # ---------------------计算入向和出向的速率---------------------
    # 计算速率
    # * 8 得到bit数
    # /1000 计算Kb
    # / x[1] 计算kbps
    # round(x, 2) 保留两位小数
    # zip把字节差列表 和 时间差列表 压到一起
    in_speed_list = list(map(lambda x: round(((x[0] * 8) / (1000 * x[1])), 2),
                            zip(diff_in_bytes_list, diff_record_time_list)))

    out_speed_list = list(map(lambda x: round(((x[0] * 8) / (1000 * x[1])), 2),
                            zip(diff_out_bytes_list, diff_record_time_list)))

    # 切掉第一个时间记录点，剩下为速率的记录时间
    record_time_list = record_time_list[1:]

    # 开始数据清洗
    clean_record_time_list = []
    clean_in_speed_list = []
    clean_out_speed_list = []

    for r, i, o in zip(record_time_list, in_speed_list, out_speed_list):
        if i > 0 and o > 0:  # 如果入向和出向速率都大于0，写入清洗后数据
            clean_record_time_list.append(r)
            clean_in_speed_list.append(i)
            clean_out_speed_list.append(o)

    # print(clean_record_time_list)
    # print(clean_in_speed_list)
    # print(clean_out_speed_list)

    # ========== 新增：计算循环复用的样式/颜色索引 ==========
    style_count = len(line_style_list)
    color_count = len(color_list)
    style_idx = count % style_count   # 取模，循环复用线条样式
    color_idx = count % color_count   # 取模，循环复用颜色

    # 写入数据到lines_list
    # 写入数据到lines_list（改用 style_idx/color_idx 作为索引）
    in_speed_lines_list.append([clean_record_time_list,
                                clean_in_speed_list,
                                line_style_list[style_idx],  # 替换为 style_idx
                                color_list[color_idx],       # 替换为 color_idx
                                f"RX:{device_ip}:{interface_name}"])
    out_speed_lines_list.append([clean_record_time_list,
                                clean_out_speed_list,
                                line_style_list[style_idx],  # 替换为 style_idx
                                color_list[color_idx],       # 替换为 color_idx
                                f"TX:{device_ip}:{interface_name}"])
    
    # -------- 保存“入向速率图” --------
    in_save_name = f"{device_ip}_rx.png"  # 文件名：device_ip_rx.png
    in_save_path = os.path.join(os.path.dirname(__file__), in_save_name)
    mat_line(in_speed_lines_list, '入向速率', '记录时间', 'kbps', save_path=in_save_path)

    # -------- 保存“出向速率图” --------
    out_save_name = f"{device_ip}_tx.png"  # 文件名：device_ip_tx.png
    out_save_path = os.path.join(os.path.dirname(__file__), out_save_name)
    mat_line(out_speed_lines_list, '出向速率', '记录时间', 'kbps', save_path=out_save_path)

    count += 1

