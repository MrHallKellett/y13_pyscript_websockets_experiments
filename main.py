from flask import Flask, jsonify, render_template, session, request, Response, redirect, flash
from flask_cors import CORS
from os import environ
from uuid import uuid4
from json import dumps, loads
##############################
from flask_sock import Sock
##############################
from helpers import source_questions
from random import randrange
from markupsafe import Markup
####################################
from models import Game, Player, Question

colours = ["red", "blue", "orange", "pink", "yellow"]
questions = dumps(source_questions(10))

GAME_DUMMY = Game("a dummy game", 10, 30, 10, "admin")


class MathQuizGame:

    def __init__(self):
        # Flask and WebSocket stuff
        app = Flask(__name__)    
        sock = Sock(app)
        sock.init_app(app)    
        app.config.update(dict(DEBUG=True))
        app.secret_key = uuid4().hex
        CORS(app)
        self.__app = app
        self.__sock = sock       
        self.register_routes()

        self.__current_games = {GAME_DUMMY.get_id():GAME_DUMMY}
        
    

    def register_routes(self):
        self.__app.add_url_rule('/', '__menu', self.__menu)
        self.__app.add_url_rule('/game/<game_id>', '__game', self.__game)

        @self.__sock.route('/send')
        def echo(ws):
            ws.send(dumps({"mode":1, "data":self._get_game_list()}))    # send initial game list
            while True:            
                data = loads(ws.receive())
                print(data)
                mode = data["mode"]
                msg  = data["message"]
                if mode == 0:       # new username
                    response = {"message":self._set_username(msg)}
                elif mode == 1:     # new game
                    self._create_new_game(msg)
                    response = self._get_game_list()
                elif mode == 2:     # join game
                    response = self._join_game(msg)
                elif mode == 3:     # new answer
                    response = self._check_answer(msg)
                elif mode == 5:     # check num secs until game start
                    game_id = msg["game_id"]
                    current_game = self.__get_game_by_id()
                    response = current_game.get_secs_til_start()
                               
                ws.send(dumps({"mode":mode, "data":response}))
    
    def __menu(self):
        session['current_game'] = GAME_DUMMY.get_id()
        return render_template("menu.html")

    def __game(self):
        game_id = session.get("current_game")
        if game_id is None:
            flash("No game was selected.")
            return redirect(f"game/{game_id}")
        else:
            return render_template("game.html", game_id=game_id)    
    
    def _set_username(self, username):
        session['username'] = username
        print("new username is", username)
        return f"Your username has been set to {username}."
    
    def _join_game(self, game_id):
        session['current_game'] = game_id
        return {"message":f"You will be joining game {game_id}."}
    
    def _create_new_game(self, game_data):
        user = session['username']
        name = game_data["name"]
        max_players = game_data["max_players"]
        delay = game_data["delay"]
        num_questions = game_data["num_questions"]
        owner = user
        new_game = Game(name, max_players, delay, num_questions, owner)
        self.__current_games[new_game.get_id()] = new_game
        print("Created a new game based on", game_data)

    def _get_game_list(self):
        games = {id_:game.get_menu_display() for id_, game in self.__current_games.items()}
        return {"games":games, "message":"List of available games updated"}                    
        
    def _get_game_by_id(self, game_id):
        return self.__curent_games[game_id]

    def run(self, host="0.0.0.0", port=8000):
        self.__app.run(host=host, port=port)



####################################

if __name__ == "__main__":

    server = MathQuizGame()




    server.run()