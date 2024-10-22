from asyncio import ensure_future

from pyodide.ffi import create_proxy
from js import WebSocket, console, document, location
from json import dumps, loads

feedback = document.getElementById("feedback")
available_games = document.getElementById("available_games")

# Replace with your WebSocket server URL
WEBSOCKET_URL = 'ws://' + location.host + "/send"
ws = WebSocket.new(WEBSOCKET_URL)


def process_message(event):
    data = loads(event.data)
    print(data)
    mode = data["mode"]
    data  = data["data"]    
    if mode == 0:
        feedback.innerHTML = data["message"]
    elif mode == 1:
        update_game_menu(data["games"])
        feedback.innerHTML = data["message"]
    elif mode == 2:
        feedback.innerHTML = data["message"] 

def show_error(msg):
    feedback.innerHTML = msg


message_proxy = create_proxy(process_message)
ws.addEventListener("message", message_proxy)
