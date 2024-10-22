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
    # modes 0, 1 & 2 for main menu screen only.
    # modes 3, 4 & 5 for game screen only.
    if mode == 0:
        show_msg(data["message"])
    elif mode == 1:
        update_game_menu(data["games"])
        show_msg(data["message"])
    elif mode == 2:
        show_msg(data["message"])
    elif mode == 5:
        update_countdown_timer(data["message"])

def show_msg(msg):
    flashes = document.getElementById("flashes")
    new_msg = document.createElement("li")
    new_msg.innerHTML = msg
    flashes.appendChild(new_msg)


message_proxy = create_proxy(process_message)
ws.addEventListener("message", message_proxy)
