import socket
import sys
import struct
import hashlib
import pickle

# Bind UDP server to listen on all interfaces on port 6666
address= ('0.0.0.0', 6666)
socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_udp.bind(address)

print("UDP server is listening on port 6666 for receiving data...")

while True:
    try:
        # receive the data, buffer size is 512 bytes
        received_data,client_addr = socket_udp.recvfrom(512)

        # 2. 按固定长度拆分三个部分
        received_header = received_data[0:16]          # 头部（16字节）
        data_pickle_received = received_data[16:496]   # 数据部分（16+480=500）
        md5_recv = received_data[496:512]     # MD5校验（500+16=516，即512字节）

        # 重新计算md5 checksum
        m5d_value = hashlib.md5(data_pickle_received).digest() 

        # unpack header
        version, packet_type, seq_id, data_len = struct.unpack('!HHIQ', received_header)

        # if local md5 is same as the received md5, then the data is correct
        if md5_recv == m5d_value:
            print('=' * 80)
            print(f"{'数据来自于':<30}：{str(client_addr)}")
            print(f"{'数据序列号':<30}：{seq_id}")
            print(f"{'数据长度为':<30}：{data_len}")
            print(f"{'数据内容为':<30}：{str(pickle.loads(data_pickle_received))}")
        else:
            print('MD5校验错误！')

    except KeyboardInterrupt:
        sys.exit()              