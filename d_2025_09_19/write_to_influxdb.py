import sys
import os
from pathlib import Path
from datetime import datetime


from influxdb import InfluxDBClient
from pytz import UTC  # for 1.x version

# 获取当前脚本的绝对路径所在目录
current_script_dir = os.path.dirname(os.path.abspath(__file__))
# 获取上层目录的路径
parent_dir = os.path.dirname(current_script_dir)

# 构建目标目录 (2025-09-18) 的绝对路径
target_dir = os.path.join(parent_dir, "2025-09-18")

# 将目标目录添加到模块搜索路径
sys.path.append(target_dir)

from snmp_v2_4_get_all import snmpv2_get_all

# get the db password
influxdb_pwd = os.getenv("influxdb_pwd")
if influxdb_pwd is None:
    # 可以选择记录日志、抛出异常或采取其他恢复措施
    sys.exit("错误：未找到 'influxdb_pwd' 环境变量。请检查环境配置。")
             

# InfluxDB vars
INFLUXDB_HOST = "localhost"    # The container is running locally
INFLUXDB_PORT = 8086           
INFLUXDB_USER = "qytdbuser"    
INFLUXDB_PASSWORD = influxdb_pwd
INFLUXDB_DATABASE = "qytdb"    

# Create influxDB connection
client = InfluxDBClient(
    host=INFLUXDB_HOST,
    port=INFLUXDB_PORT,
    username=INFLUXDB_USER,
    password=INFLUXDB_PASSWORD,
    database=INFLUXDB_DATABASE
)

# Create the DB
client.create_database(INFLUXDB_DATABASE)

def get_info_writedb(ip_address, community):
    '''
    Get information from the routers through SNMPv2, write the DB
    '''
    router_all_snmp_dict = snmpv2_get_all(ip_address, community)
    

    # Prepare the cpu, memory utilization data
    data_point = {
        "measurement": "router_metrics",  # table name
        "tags": {                         # tags, unchanged fields
            "ip_address": ip_address,
            "device_type": "IOS-XE"
        },
        "time": datetime.now(tz=UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ"), 
        "fields": {
            "cpu_usage": router_all_snmp_dict["cpu_usage"],               # int类型
            "mem_usage_percent": router_all_snmp_dict["mem_usage_percent"], # float类型
            "mem_usage": router_all_snmp_dict["mem_usage"],               # int类型
            "mem_free": router_all_snmp_dict["mem_free"],                 # int类型
            "device_ip": router_all_snmp_dict["device_ip"]                # str类型（设备IP字符串）
        }                       
    }
    
    # 写入数据到InfluxDB
    client.write_points([data_point])
    print(f'data from {data_point["tags"]["ip_address"]} is written to the measurement: {data_point["measurement"]} ')

    # Write inrefaces data to the DB
    #if_bytes_body = []  # 用于存储多个接口的字典

    for if_info in router_all_snmp_dict.get('interface_list',[]):
        if if_info.get('in_bytes') and if_info.get('out_bytes'):
            if_info_dict = {
                            "measurement": "if_monitor",   # table name
                            "time": datetime.now(tz=UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),  # timestamp, key of the time series DB
                            "tags": {                      # tags for filter
                                "device_ip": router_all_snmp_dict.get('device_ip'),
                                "device_type": "IOS-XE",
                                "interface_name": if_info.get('interface_name')
                            },
                            "fields": {                    # 字段，用于存储数据
                                "in_bytes": if_info.get('in_bytes'),
                                "out_bytes": if_info.get('out_bytes'),
                            },
                        }
            
        # 写入数据到InfluxDB
        client.write_points([if_info_dict])

    print(f'data from {if_info_dict["tags"]["device_ip"]} is written to the measurement: {if_info_dict["measurement"]} ')




if __name__ == '__main__':
    ip_address_list = ['10.128.1.51', '10.128.1.91']
    community = 'tcpipro'

    for ip in ip_address_list:
        get_info_writedb(ip, community)
    
    # 关闭连接
    client.close()