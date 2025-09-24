from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# 导入之前定义的模型类（确保与你的模型文件路径一致）
from create_postgresql_db import Base, Router, Interface, OSPFProcess, Area, OSPFNetwork


# 1. 配置数据库连接
engine = create_engine('postgresql+psycopg2://qytangdbuser:Cisco0123@127.0.0.1:5432/qytangdb')
Session = sessionmaker(bind=engine)
session = Session()

# 数据原始信息
# 设备接口信息
c8kv1_ifs = [{'ifname': "GigabitEthernet1", 'ip': "10.128.1.51", 'mask': "255.255.255.0"},
             {'ifname': "Loopback0", 'ip': "1.1.1.1", 'mask': "255.255.255.255"}]

c8kv2_ifs = [{'ifname': "GigabitEthernet1", 'ip': "10.128.1.91", 'mask': "255.255.255.0"},
             {'ifname': "Loopback0", 'ip': "2.2.2.2", 'mask': "255.255.255.255"}]

# 设备OSPF信息
c8kv1_ospf = {"process_id": 1,
              "router_id": "1.1.1.1",
              "areas": [{'area_id': 0, 'networks': [{'ip': "10.128.1.51", 'wildmask': "0.0.0.255"},
                                                     {'ip': "1.1.1.1", 'wildmask': "0.0.0.0"}]}]}

c8kv2_ospf = {'process_id': 1,
              "router_id": "2.2.2.2",
              "areas": [{'area_id': 0, 'networks': [{'ip': "10.128.1.91", 'wildmask': "0.0.0.255"},
                                                     {'ip': "2.2.2.2", 'wildmask': "0.0.0.0"}]}]}

username = 'admin'
password = 'cisco123'

# 汇总后数据
all_network_data = [{'ip': "10.128.1.51",
                     'router_name': 'C8Kv1',
                     'username': username,
                     'password': password,
                     'interfaces': c8kv1_ifs,
                     'ospf': c8kv1_ospf},
                    {'ip': "10.128.1.91",
                     'router_name': 'C8Kv2',
                     'username': username,
                     'password': password,
                     'interfaces': c8kv2_ifs,
                     'ospf': c8kv2_ospf}]


# 3. 循环处理数据并插入数据库
if __name__ == "__main__":

    try:
        for router_data in all_network_data:
            # 3.1 创建路由器记录
            router = Router(
                router_name=router_data['router_name'],
                ip=router_data['ip'],
                username=router_data['username'],
                password=router_data['password']
            )
            session.add(router)
            session.flush()  # 刷新会话，获取刚插入的router.id（用于后续外键关联）

            # 3.2 创建接口记录（关联到当前路由器）
            for if_data in router_data['interfaces']:
                interface = Interface(
                    router_id=router.id,
                    interface_name=if_data['ifname'],
                    ip=if_data['ip'],
                    mask=if_data['mask']
                )
                session.add(interface)

            # 3.3 创建OSPF进程记录（关联到当前路由器）
            ospf_data = router_data['ospf']
            ospf_process = OSPFProcess(
                router_id=router.id,
                processid=ospf_data['process_id'],
                routerid=ospf_data['router_id']
            )
            session.add(ospf_process)
            session.flush()  # 获取ospf_process.id

            # 3.4 创建区域记录（关联到当前OSPF进程）
            for area_data in ospf_data['areas']:
                area = Area(
                    ospfprocess_id=ospf_process.id,
                    area_id=area_data['area_id']
                )
                session.add(area)
                session.flush()  # 获取area.id

                # 3.5 创建OSPF网络记录（关联到当前区域）
                for network_data in area_data['networks']:
                    ospf_network = OSPFNetwork(
                        area_id=area.id,
                        network=network_data['ip'],
                        wildmask=network_data['wildmask']
                    )
                    session.add(ospf_network)

        # 提交所有数据（事务）
        session.commit()
        print("数据插入成功！")

    except Exception as e:
        # 出错时回滚
        session.rollback()
        print(f"插入失败：{str(e)}")

    finally:
        # 关闭会话
        session.close()