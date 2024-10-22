from asyncio import ensure_future

from pyodide.ffi import create_proxy
from js import WebSocket, console, document, location, localStorage
from json import dumps, loads
from uuid import uuid4

feedback = document.getElementById("feedback")

available_games = document.getElementById("available_games")

# Replace with your WebSocket server URL
WEBSOCKET_URL = 'ws://' + location.host + "/" + mode
ws = WebSocket.new(WEBSOCKET_URL)

token = None


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
        print("updating countdown")
        update_countdown_timer(data["message"])

def show_msg(msg):
    flashes = document.getElementById("flashes")
    new_msg = document.createElement("li")
    new_msg.innerHTML = msg
    flashes.appendChild(new_msg)

def handshake(event):
    global token
    print("WebSocket connection established!")
    

    # handshake
    token = localStorage.getItem("token")
    if token is None:
        token = uuid4().int
        localStorage.setItem("token", token)

    ws.send(dumps({"message":"hello", "mode":9, "token":token}))


message_proxy = create_proxy(process_message)
ws.addEventListener("message", message_proxy)
ws.on_open = handshake

