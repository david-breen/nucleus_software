import sys
import time
from pynng import Pub0,Sub0,Timeout
import json
import base64
import threading
import asyncio

avionics_address = 'tcp://127.0.0.1:20000'
altitude_address = 'tcp://127.0.0.1:20001'
balloon_address = 'tcp://127.0.0.1:20002'
power_address = 'tcp://127.0.0.1:20003'


def data_to_send():
    json_data = {
        "gps": (44,-77), 
        "pressure": 44.8}
    data = json.dumps(json_data)
    return data.encode('utf-8')

async def open_comms(address,sec,mes):
    with Pub0(listen=address) as alt_pub:
        time.sleep(0.25)
        global next_msg
        for _ in range(50):
            next_msg = time.time() + sec
            alt_pub.send(b'altitude:' + data_to_send())
            print(mes)
            print(time.time())
            await asyncio.sleep(next_msg-time.time())


async def main():
    L1 = loop.create_task(open_comms(altitude_address,0.1,"1"))
    L2 = loop.create_task(open_comms(avionics_address,0.2,"2"))
    L3 = loop.create_task(open_comms(balloon_address,0.4,"3"))
    L4 = loop.create_task(open_comms(power_address,0.1,"4"))
    await asyncio.wait([L1,L2,L3,L4])


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except Exception as e:
        pass
    finally:
        loop.close()