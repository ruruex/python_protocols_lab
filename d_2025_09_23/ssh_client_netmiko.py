from netmiko import Netmiko
import yaml
import os
from jinja2 import Template
import sys
from pathlib import Path

# 获取当前文件所在目录的父目录（项目根目录）并添加到Python路径
current_file = Path(__file__)
current_dir = current_file.parent
sys.path.append(str(current_dir))

# flake8: noqa
#from netmiko_1_show_client import device_ip, username, password


def netmiko_config_cred(host,
                        username,
                        password,
                        cmds_list,
                        device_type='cisco_ios',
                        verbose=False,
                        ssh_port=22):
    device_info = {
                    'host': host,
                    'username': username,
                    'password': password,
                    'device_type': device_type,
                    # 'global_delay_factor': 2,  # 增加全局延迟因子
                    'session_log': 'session.log',  # 启用会话日志
                    'port': ssh_port
    }
    try:
        net_connect = Netmiko(**device_info)

        if verbose:
            output = net_connect.send_config_set(cmds_list) # 自动进入enable 和config mode
            return output
        else:
            net_connect.send_config_set(cmds_list)
        net_connect.disconnect()

    except Exception as e:
        print(f'connection error ip: {host} error: {str(e)}')
        return


def config_cmd_list(config_direction_name):
    # 根据配置的方向, 读取对应的配置文件, 并根据配置文件生成对应的配置命令
    # --- 配置模板文件
    config_template_dir = f'{current_dir}{os.sep}config-template'
    template_file_name = f'{config_direction_name}.jinja2'
    # --- 配置数据文件
    config_data_dir = f'{current_dir}{os.sep}/config-data'
    data_file_name = f'{config_direction_name}.yaml'

    with open(f'{config_data_dir}{os.sep}{data_file_name}') as data_f:
        # 读取配置数据文件
        data = yaml.safe_load(data_f.read())
        # 读取配置模板文件
        with open(f'{config_template_dir}{os.sep}{template_file_name}') as template_f:
            # 读取配置模板文件
            template = Template(template_f.read())
            # 渲染产生配置命令
            config_str = template.render(data)
            # if line.strip() 确认strip后不为空
            return [line.strip() for line in config_str.split('\n') if line.strip()]


if __name__ == '__main__':
    # 这是配置的方向, 会根据配置的方向, 读取对应的配置文件, 并根据配置文件生成对应的配置命令
    # config_direction = 'snmp'
    config_direction = 'ospf'
    # ------------------------------------------------------------
    config_cmds = config_cmd_list(config_direction)
    '''
    print(netmiko_config_cred(device_ip,
                              username,
                              password,
                              config_cmds,
                              'cisco_ios',
                              verbose=True))
    '''
