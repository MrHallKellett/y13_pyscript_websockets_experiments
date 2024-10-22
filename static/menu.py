from asyncio import ensure_future
from pyodide.ffi import create_proxy
from js import WebSocket, console, document, location
from json import dumps, loads


feedback = document.getElementById("feedback")

available_games = document.getElementById("available_games")


def set_username(event):
    username = event.target.value
    ws.send(dumps({"message":username, "mode":0}))

def set_game(event):
    game_id = available_games.selectedOptions[0].id    
    ws.send(dumps({"message":game_id, "mode":2}))

def create_game(event):
    print("running submit proxy")
    
    username = document.getElementById("username").value
    if username == "":
        show_msg("Enter username first.")
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
    
    for id_, game in games.items():
        this_game = document.createElement("option")
        available_games.appendChild(this_game)
        this_game.setAttribute("value", game)
        this_game.innerHTML = game
        this_game.setAttribute("id", id_)
        




## main menu event handling
    
username_field = document.getElementById("username")
change_user_proxy = create_proxy(set_username)
username_field.addEventListener("change", change_user_proxy)

game_select_dd = document.getElementById("available_games")
change_game_proxy = create_proxy(set_game)
game_select_dd.addEventListener("change", change_game_proxy)


create_game_btn = document.getElementById("create_game")
submit_proxy = create_proxy(create_game)
create_game_btn.addEventListener("click", submit_proxy)

