from create_int_monitor_db import InterfaceMonitor,engine,db_file_name,create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError


import sys,os
import datetime

# 获取当前脚本所在目录的绝对路径（d_2025_09_22）
current_script_dir = os.path.dirname(os.path.abspath(__file__))
# 计算 python_protocol 目录的绝对路径（当前目录的父目录）
python_protocol_dir = os.path.dirname(current_script_dir) 
# 将父目录添加到 sys.path
if python_protocol_dir not in sys.path:
    sys.path.append(python_protocol_dir)

from d_2025_09_18.snmp_v2_4_get_all import snmpv2_get_all

def get_int_info(ip_address,community):
    """
    Use SNMPv2 get to retrive the routers interface couters, remove unused fields
    """
    router_all_snmp_dict = snmpv2_get_all(ip_address,community)
    
    # Remove unused fields
    keys_to_pop = ['cpu_usage','mem_usage_percent','mem_usage','mem_free','hostname']
    for key in keys_to_pop:
        router_all_snmp_dict.pop(key) 

    return router_all_snmp_dict
 

def write_to_int_db(ip_address, community):
    '''
    Write the DB
    '''
    # Suggest to have session created in function, not global object
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Get the filter dictionary from the devices
        router_int_dict = get_int_info(ip_address, community)
        
        # 提取设备IP
        device_ip = router_int_dict['device_ip']

        # 遍历接口列表，创建 InterfaceMonitor 对象
        interface_monitors_to_add = []
        for interface in router_int_dict['interface_list']:
            new_record = InterfaceMonitor(
                device_ip=device_ip,
                interface_name=interface['interface_name'],
                in_bytes=interface['in_bytes'],
                out_bytes=interface['out_bytes'],
                record_datetime=datetime.datetime.now()  # 使用当前时间作为记录时间
            )
            interface_monitors_to_add.append(new_record)

        #print(f'interface_monitors_to_add is {interface_monitors_to_add}')
        # Commit the change
        session.add_all(interface_monitors_to_add)
        session.commit() # return None
        print(f"成功为设备 {device_ip} 添加了 {len(interface_monitors_to_add)} 条接口监控记录。")
    
    except SQLAlchemyError as e:
        # 如果发生数据库错误，回滚当前事务
        session.rollback()
        print(f"为设备 {ip_address} 写入数据库时发生错误，事务已回滚: {e}")
    except Exception as e:
        # 处理其他可能的异常（如get_int_info中的网络请求错误）
        print(f"处理设备 {ip_address} 时发生未知错误: {e}")
    finally:
        # 无论成功与否，最终都要确保会话被关闭
        session.close()


if __name__ == "__main__":
    ip_address_list = ['10.128.1.51','10.128.1.91']
    community = 'tcpipro'

    for ip in ip_address_list:
        write_to_int_db(ip,community)
