from sqlalchemy.orm import sessionmaker
from create_cpu_mem_db import RouterMonitor, db_file_name,create_engine
from datetime import datetime, timedelta

import os
from pathlib import Path

engine = create_engine(f'sqlite:///{db_file_name}?check_same_thread=False')

Session = sessionmaker(bind=engine)
session = Session()

# get 5 mins before time
five_minutes_before = datetime.now() - timedelta(minutes=5)

# get cpu data 
def cpu_query(device_ip):
    time_list = []
    cpu_list = []

    # 把结果写入 time_list 和 cpu_list 的列表，只取五分钟之内的数据
    for record in session.query(RouterMonitor).filter(RouterMonitor.device_ip == device_ip).all():
        time_list.append(record.record_datetime)  # Keep as datetime obj for matplotlib
        cpu_list.append(record.cpu_usage)

    return cpu_list,time_list

def memory_query(device_ip):
    time_list = []
    mem_list = []

    # 把结果写入 time_list 和 mem_list 的列表，只取五分钟之内的数据
    for record in session.query(RouterMonitor).filter(RouterMonitor.device_ip== device_ip).all():
        time_list.append(record.record_datetime) # Keep as datetime obj for matplotlib
        mem_list.append(record.mem_usage_percent)

    return mem_list,time_list


if __name__ == '__main__':
    device_ip_list = ['10.128.1.51','10.128.1.91']
    for deivce_ip in device_ip_list:
        print(cpu_query(deivce_ip))
        print(memory_query(deivce_ip))