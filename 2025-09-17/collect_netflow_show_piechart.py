from netmiko import ConnectHandler
from netmiko.exceptions import NetMikoTimeoutException, NetMikoAuthenticationException


from python_matplotlib_pie_chart import mat_bing

import os,re

# Router connection info
cisco_pwd = os.environ.get('cisco_pwd')
device = {
    "device_type": "cisco_ios",
    "host": "10.128.1.51",
    "username": "admin",
    "password": cisco_pwd,
    "secret": cisco_pwd  # if needed
}

# Connect to device
try:
    conn = ConnectHandler(**device)
    conn.enable()  # enter enable mode if required
except NetMikoTimeoutException:
    print("Timeout, check your connection")
    exit(1)
except NetMikoAuthenticationException:
    print("Authentication error")
    exit(1)
except Exception as e:
    print(f"Unknow errors: {e}")
    exit(1)

# Run the CLI command
output = conn.send_command("show flow monitor name qytang-monitor cache format csv")

def parse_netflow_data(output):
    """
    Retrive the netflow data and extract the apps name and count in bytes
    
    Args:
        output (str): raw content from the network device
        
    Returns:
        tuple: include app names and counts in bytes
    """
    name_list = []
    count_list = []
    capture = False

    for line in output.splitlines():
        line = line.strip()
        if line.startswith("APP NAME,bytes"):  # match the header row
            capture = True 
            continue
        if capture and line:
            line_refine = re.split("\s|,",line)
            name_list.append(line_refine[1]) # app name remove layer7
            count_list.append(line_refine[2]) # port prefix, app bytes
    
    return name_list, count_list

# Parse CSV portion
name_list, count_list = parse_netflow_data(output)

mat_bing(name_list, count_list,"第三天作业netflow")