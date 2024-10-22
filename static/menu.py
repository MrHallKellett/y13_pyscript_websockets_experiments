from asyncio import ensure_future
from pyweb import pydom
from pyodide.ffi import create_proxy
from js import document, WebSocket, location
from pyodide.http import pyfetch
from js import WebSocket, console, document
import json



container = pydom["#container"][0]
feedback =  pydom["#feedback"][0]



async def set_username(event):
    new_username = event.target.value    
    print(f"Using pyfetch to send new_username to server")
    result = await pyfetch(
        url=f"/set_username/{new_username}",
        method="GET",       
    )
    


# Replace with your WebSocket server URL
WEBSOCKET_URL = 'ws://' + location.host + "/send"
print(WEBSOCKET_URL)

ws = WebSocket.new(WEBSOCKET_URL)


def set_username(event):
    username = event.target.value
    ws.send(json.dumps({"message":username, "mode":0}))

def process_message(event):
    data = event.data
    print("got data", data)
    feedback.html = data


username_field = document.getElementById("set_username")
change_proxy = create_proxy(set_username)
username_field.addEventListener("change", change_proxy)



message_proxy = create_proxy(process_message)

ws.addEventListener("message", message_proxy)