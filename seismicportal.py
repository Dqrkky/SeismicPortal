import asyncio
import websockets
import datetime
import json

class WebsocketRaw:
    def __init__(self, data :dict=None, _format :any=None):
        self.data :dict = data
        self.format :any = _format
    def todict(self):
        return self.__dict__

class WebsocketPing:
    def __init__(self, time :datetime.datetime=None):
        self.type = "WebsocketPing"
        self.time :datetime.datetime = time
    def todict(self):
        return self.__dict__

class SeismicPortal:
    def __init__(self):
        self.event_handlers = {}
        self.config = {
            "getaway": "wss://www.seismicportal.eu/standing_order/websocket",
            "ping_interval": 15
        }
    def event(self, event_type=None):
        return self._register_event(event_type=event_type)
    def _register_event(self, event_type=None):
        return self.decorator(event_type) if event_type else self.decorator
    def decorator(self, event_type=None):
        if event_type:
            if event_type.__name__ not in self.event_handlers:
                self.event_handlers[event_type.__name__] = event_type
            return event_type
    async def trigger_event(self, event_name=None, event_data=None):
        if event_name and event_data:
            if event_name in self.event_handlers:
                await self.event_handlers[event_name](event_data)
    async def send_ping(self, websocket=None, ping_interval :int=None):
        if websocket and \
        ping_interval != None and isinstance(ping_interval, int):  # noqa: E711
            while True:
                await websocket.ping()
                await self.trigger_event(
                    event_name="on_websocket_ping",
                    event_data=WebsocketPing(
                      time=datetime.datetime.now()
                    )
                )
                await asyncio.sleep(ping_interval)
    async def receive_data(self, websocket=None):
        if websocket:
            while True:
                data = await websocket.recv()
                if data:
                    try:
                        loaded_data = json.loads(
                            data
                        )
                        _format = "json"
                    except Exception:
                        loaded_data = data
                        _format = "text"
                    await self.trigger_event(
                        event_name="on_websocket_raw",
                        event_data=WebsocketRaw(
                            data=loaded_data,
                            _format=_format
                        )
                    )
    async def start(self):
        if hasattr(self, "config") and self.config != None and isinstance(self.config, dict) and \
        "getaway" in self.config and self.config["getaway"] != None and isinstance(self.config["getaway"], str) and \
        "ping_interval" in self.config and self.config["ping_interval"] != None and isinstance(self.config["ping_interval"], int):  # noqa: E711
            async with websockets.connect(
                self.config["getaway"]
            ) as websocket:
                ping_task = asyncio.create_task(
                    self.send_ping(
                        websocket=websocket,
                        ping_interval=self.config["ping_interval"]
                    )
                )
                data_task = asyncio.create_task(
                    self.receive_data(
                        websocket=websocket
                    )
                )
                await asyncio.gather(
                    ping_task,
                    data_task
                )
    def run(self):
        asyncio.run(
            self.start()
        )