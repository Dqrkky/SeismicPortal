import seismicportal

sp = seismicportal.SeismicPortal()

@sp.event
async def on_websocket_raw(ctx :seismicportal.WebsocketRaw):
    print(ctx.todict())

sp.run()