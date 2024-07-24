import websockets

class WebSocketManager:
    def __init__(self, url):
        self.url = url
        self.websocket = None

    async def connect(self):
        self.websocket = await websockets.connect(self.url)

    async def send(self, message):
        await self.websocket.send(message)

    async def close(self):
        await self.websocket.close()