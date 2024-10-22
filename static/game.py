from asyncio import ensure_future
from pyodide.ffi import create_proxy
from js import WebSocket, console, document, location, setInterval
from json import dumps, loads



countdown = document.getElementById("countdown")

def update_game_menu():
    # fix later - OOP approach, abstract base class or smth
    raise NotImplementedError




def check_secs_til_game_start():
    ws.send(dumps({"message":game_id, "mode":5}))
    
def update_countdown_timer(secs):
    countdown.innerHTML = secs


setInterval(check_secs_til_game_start, 1000)