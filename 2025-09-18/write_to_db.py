import sys
import os

from create_cpu_mem_db import RouterMonitor,engine,db_file_name,create_engine
from snmp_v2_4_get_all import snmpv2_get_all
from sqlalchemy.orm import sessionmaker


# Add current path into system path env
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.extend([current_dir])


engine = create_engine(f'sqlite:///{db_file_name}?check_same_thread=False',echo=False)

Session = sessionmaker(bind=engine)
session = Session()

def get_info_writedb(ip_address, community):
    '''
    Get information from routers, write to the DB
    '''
    router_all_snmp_dict = snmpv2_get_all(ip_address,community)
    

    # remove the DB unused fields 
    router_all_snmp_dict.pop('interface_list')
    router_all_snmp_dict.pop('hostname')
    print(f'router_all_snmp_dict is {router_all_snmp_dict}')

    # write to the DB
    router_monitor_record = RouterMonitor(**router_all_snmp_dict)
    session.add(router_monitor_record)
    session.commit()

if __name__ == '__main__':
    ip_address_list = ['10.128.1.51','10.128.1.91']
    community = 'tcpipro'

    for ip in ip_address_list:
        get_info_writedb(ip,community)
