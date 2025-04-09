import seismicportal
import os

sp = seismicportal.SeismicPortal() 

def printJson(js0n :dict=None):
    if js0n != None and isinstance(js0n, dict):  # noqa: E711
        os.system("cls")
        print(seismicportal.json.dumps(obj=js0n, indent=4))

@sp.event
async def on_websocket_raw(ctx :seismicportal.WebsocketRaw):
    printJson(ctx.todict())

try:
    sp.run()
except Exception as e:
    error = {
        "error": list(e.args),
        "error_type": type(e).__name__,
        "error_module": type(e).__module__
    }
    printJson(error)