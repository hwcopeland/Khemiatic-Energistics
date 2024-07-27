import asyncio
import json
from websocket import WebSocketManager, request
from requestlib import home
from worker import movecoord



async def main():
    liq_url = "ws://10.255.255.6:7125/websocket"
    liq = WebSocketManager(liq_url)
    try:
        await liq.connect()
        await request(home(), liq)
        await request(movecoord(x=110,y=110,z=20,f=4000), liq)
        vial = (25,25)
        await request(movecoord(x=vial[0],y=vial[1],z=20,f=4000), liq)
        ## We would prefer to use vial ids as a request to move to funtion. ie move(vial_id, position)
        # The issue would be deciding how to store the vial ids and their positions.
        # should this be in a database or a json file?


    except Exception as e:
        print(f"Connection failed: {e}")
    finally:
        await liq.close()

asyncio.run(main())