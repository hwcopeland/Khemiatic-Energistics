import asyncio
import json
from websocket import WebSocketManager
from requestlib import home

async def request(command, websocket):
    await websocket.send(json.dumps(command))
    print(f"> Sent: {json.dumps(command, indent=2)}")
    response = await websocket.recv()
    print(f"< Received: {json.dumps(json.loads(response), indent=2)}")
    return json.loads(response)

MOONRAKER_WS_URL = "ws://10.255.255.6:7125/websocket"

async def main():
    url = MOONRAKER_WS_URL
    ws_manager = WebSocketManager(url)
    try:
        await ws_manager.connect()
        await request(home(), ws_manager.websocket)


    except Exception as e:
        print(f"Connection failed: {e}")
    finally:
        await ws_manager.close()

asyncio.run(main())