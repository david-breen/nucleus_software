import sys
import time
from pynng import Pub0,Sub0,Timeout
import json

avionics_address = 'tcp://127.0.0.1:20000'
altitude_address = 'tcp://127.0.0.1:20001'
balloon_address = 'tcp://127.0.0.1:20002'
power_address = 'tcp://127.0.0.1:20003'

mes_rec = []

def data_to_send():
    json_data = {
    "gps": (44,-77), 
    "pressure": 44.8, 
    "temperature": 10, 
    "imu": [.3, .4, 1.01, 3, 5, 2]}

    data = json.dumps(json_data)
    return data.encode('utf-8')

def extract_data(comp_data, prefix):
#extract_data is fed a list of string serialized json messages
#it then deserializes them into readable json
    unpacked_data = []
    while len(comp_data) > 0:
        #takes the encoded string serialized json data and stores it as readable json
        unpacked = json.loads(comp_data.pop(0).decode('utf-8').strip(prefix))
        unpacked_data.append(unpacked)
        print(unpacked)
    return unpacked_data

def main():
    with Pub0(listen=avionics_address) as avi_pub, \
            Sub0(dial=altitude_address, recv_timeout=300) as sub0: #pubsub obj constructors

        sub0.subscribe(b'altitude') #sub to the altitude topic
        sub0.subscribe(b'avionics') #sub to the avionics topic
        sub0.recv_buffer_size = 128
        time.sleep(0.05)

        for _ in range(10):
            avi_pub.send(b'avionics:' + data_to_send())
            try:
                mes_rec.append(sub0.recv())
            except Timeout:
                print('Timeout, no message recieved')
            time.sleep(0.25)

        extract_data(mes_rec,"altitude:")

if __name__ == "__main__":
    main()