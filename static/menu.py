from asyncio import ensure_future
from pyweb import pydom
from pyodide.ffi import create_proxy
from js import document, WebSocket, location
from pyodide.http import pyfetch
from js import WebSocket, console, document
from json import dumps, loads




feedback =  pydom["#feedback"][0]
available_games = pydom["#available_games"][0]



# Replace with your WebSocket server URL
WEBSOCKET_URL = 'ws://' + location.host + "/send"
print(WEBSOCKET_URL)

ws = WebSocket.new(WEBSOCKET_URL)


def set_username(event):
    username = event.target.value
    ws.send(dumps({"message":username, "mode":0}))

def create_game(event):
    print("running submit proxy")
    
    username = document.getElementById("username").value
    if username == "":
        show_error("Enter username first.")
        return
    
    name = document.getElementById("name").value
    max_players = document.getElementById("max_players").value
    num_questions = document.getElementById("num_questions").value
    delay = document.getElementById("delay").value

    ws.send(dumps({"message":{"name":name,
                              "max_players":max_players,
                              "num_questions":num_questions,
                              "delay":delay
                             },
                    "mode":1}
            ))
    

    


def update_game_menu(games):
    available_games.html = ""
    for game in games:
        this_game = available_games.create("option")
        this_game.value = game
        this_game.html = game

def process_message(event):
    data = loads(event.data)
    print(data)
    mode = data["mode"]
    data  = data["data"]

    
    if mode == 0:
        feedback.html = data["message"]
    elif mode == 1:

        update_game_menu(data["games"])
        feedback.html = data["message"]

def show_error(msg):
    feedback.html = msg


username_field = document.getElementById("username")
change_proxy = create_proxy(set_username)
username_field.addEventListener("change", change_proxy)

message_proxy = create_proxy(process_message)
ws.addEventListener("message", message_proxy)

create_game_btn = document.getElementById("create_game")
submit_proxy = create_proxy(create_game)
create_game_btn.addEventListener("click", submit_proxy)