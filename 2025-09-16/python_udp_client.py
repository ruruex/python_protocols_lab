import socket
import struct
import hashlib
import pickle

from datetime import datetime

def udp_send_data(ip, port, data_list):
    '''
    Send udp with the following header
    data_list: the payload data list
    port: destination port number
    ip: the target IP
    '''
    # Build address object
    address = (ip, port)

    # Construct the UDP datagram
    socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    version = 1
    type = 1
    seq_id =123456
    
    for data in data_list:
        # Design the header, length is 2+2+4+8=16 bytes
        header = struct.pack('!HHIQ', version, type, seq_id, len(data))

        # variable lenght data
        max_data_len = 480
        data_pickle = pickle.dumps(data)
        if len(data_pickle) > max_data_len:
            data_pickle = data_pickle[:max_data_len] # 截断
        else: # 补足到480
            data_pickle += b'\x00' * (max_data_len - len(data_pickle))

        # hash of the data in md5, 16 bytes
        md5 = hashlib.md5(data_pickle).digest()

        # Use pickle to convert data to bytes
        send_data = header + data_pickle + md5
        #print(f'send_data is {send_data}')

        # Concate and send the data and md5
        socket_udp.sendto(send_data, address)

        seq_id += 1
        print('loop is done')

    socket_udp.close()


if __name__ == "__main__":
    user_data = ['乾颐堂', [1,'qytang',3],{'qytang': 1, 'test':3},{'datetime': datetime.now()}]
    udp_send_data('10.128.1.68',6666,user_data)