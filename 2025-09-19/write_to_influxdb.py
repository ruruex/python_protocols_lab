import sys
import os
from pathlib import Path
from datetime import datetime

from influxdb import InfluxDBClient  # for 1.x version

# 获取当前脚本的绝对路径所在目录
current_script_dir = os.path.dirname(os.path.abspath(__file__))
# 获取上层目录的路径
parent_dir = os.path.dirname(current_script_dir)

# 构建目标目录 (2025-09-18) 的绝对路径
target_dir = os.path.join(parent_dir, "2025-09-18")

# 将目标目录添加到模块搜索路径
sys.path.append(target_dir)

from snmp_v2_4_get_all import snmpv2_get_all