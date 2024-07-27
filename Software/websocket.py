import asyncio
import json
import websockets

class WebSocketManager:
    def __init__(self, url):
        self.url = url
        self.websocket = None

    async def connect(self):
        self.websocket = await websockets.connect(self.url)

    async def send(self, message):
        await self.websocket.send(message)

    async def recv(self):
        return await self.websocket.recv()

    async def close(self):
        await self.websocket.close()

async def request(command, websocket):
    await websocket.send(json.dumps(command))
    print(f"> Sent: {json.dumps(command, indent=2)}")
    response = await websocket.recv()
    print(f"< Received: {json.dumps(json.loads(response), indent=2)}")
    return json.loads(response)
