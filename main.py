from flask import Flask, jsonify, render_template, \
    request, Response, redirect, flash, url_for, session
from flask_cors import CORS
from os import environ
from uuid import uuid4
from json import dumps, loads
##############################
from flask_sock import Sock
from cachelib.file import FileSystemCache
#from flask_socketio import SocketIO, emit
from flask_session import Session
##############################
from helpers import source_questions
from random import randrange
from markupsafe import Markup
####################################
from models import Game, Player, Question

colours = ["red", "blue", "orange", "pink", "yellow"]
questions = dumps(source_questions(10))

GAME_DUMMY = Game("a dummy game", 10, 30, 10, "admin")

sess = Session()

class MathQuizGame:

    def __init__(self):
        # Flask and WebSocket stuff
        app = Flask(__name__)    
        
        sock = Sock(app)
        sock.init_app(app)    

        

        app.config.update(dict(DEBUG=True))
        app.config['SESSION_TYPE'] = 'cachelib'
        app.config['SESSION_CACHELIB'] = FileSystemCache(cache_dir='flask_session', threshold=500)
        app.config['SECRET_KEY'] = uuid4().hex
        CORS(app)
        sess.init_app(app)
        self.__app = app
        self.__sock = sock     
        
        self.register_routes()
        

        self.__current_games = {GAME_DUMMY.get_id():GAME_DUMMY}

        self.__sessions = {}
        
    

    def register_routes(self):
        self.__app.add_url_rule('/', '__menu', self.__menu)

        @self.__app.route('/game/<token>')
        def game_route(token):
            return self.__game(token)

       
        

        @self.__sock.route('/game')
        def game_echo(ws):
            current_game = self.__get_current_game()

            ws.send(dumps({"mode":6, "data":current_game.get_question_display()}))    # send questions


            while True:
                data = loads(ws.receive())
                print(data)
                mode  = data["mode"]
                msg   = data["message"]
                token = data["token"]
                if mode == 4:     # new player joined server
                    username = self.__get_session_data(token, 'username')
                    current_game.add_player(username)
                    new_player = current_game.get_newest_player()
                    response = {"message":new_player.get_join_message()}
                if mode == 5:     # check num secs until game start                                        
                    response = {"message":current_game.get_secs_til_start()}

                ws.send(dumps({"mode":mode, "data":response}))


        @self.__sock.route('/menu')
        def menu_echo(ws):
            # handshake
            data = loads(ws.receive())   
            token = data["token"]   
            self.__sessions[token] = {}
            ws.send(dumps({"mode":1, "data":self._get_game_list()}))    # send initial game list
            while True:            
                data = loads(ws.receive())
                print(data)
                mode = data["mode"]
                msg  = data["message"]
                token = data["token"]
                if mode == 0:       # new username
                    response = {"message":self._set_username(msg, token)}
                elif mode == 1:     # new game
                    self._create_new_game(msg, token)
                    response = self._get_game_list()
                elif mode == 2:     # set game to join
                    response = self._set_game_to_join(msg, token)
                elif mode == 3:     # new answer
                    response = self._check_answer(msg)
                
                               
                ws.send(dumps({"mode":mode, "data":response}))
    
    def __menu(self):
        
        token = uuid4().int     
        
        return render_template("menu.html")

    def __game(self, token):

        print("checking session data via token", token)
        print("session contents is")
        print(self.__sessions)
            
        game_id = self.__get_session_data(token, 'current_game')
        username = self.__get_session_data(token, 'username')

        print("current game", game_id, "current username", username)
        if game_id is None:
            flash("No game was selected.")
            return redirect(url_for("__menu"))
        elif username is None:
            flash("No username was entered.")
            return redirect(url_for("__menu"))
        else:            
            self.__get_current_game().add_player(username)
            return render_template("game.html", game_id=game_id)  

  
    
    def _set_username(self, username, token):        
        self.__set_session_data(token, 'username', username)
        print("new username is", username)

        game_id = session.get('current_game')
        return f"Your username has been set to {username}. Currently playing game {game_id}"
    
    def _set_game_to_join(self, game_id, token):        
        username = self.__get_session_data(token, 'username')       
        self.__set_session_data(token, 'current_game', game_id)

        return {"message":f"You will be joining game {game_id}. Current user is {username}"}
    
    def _create_new_game(self, game_data, token):
        username = self.__get_session_data(token, 'username')
        name = game_data["name"]
        max_players = int(game_data["max_players"])
        delay = game_data["delay"]
        num_questions = int(game_data["num_questions"])
        owner = username
        new_game = Game(name, max_players, delay, num_questions, owner)
        self.__current_games[new_game.get_id()] = new_game
        print("Created a new game based on", game_data)

    def _get_game_list(self):
        games = {id_:game.get_menu_display() for id_, game in self.__current_games.items()}
        return {"games":games, "message":"List of available games updated"}                    
        
    def _get_game_by_id(self, game_id):
        return self.__current_games[game_id]

    def __get_current_game(self, token):
        game_id = self.__get_session_data(token, 'current_game')
        return self._get_game_by_id(game_id)
    
    def __set_session_data(self, token, field, value):
        self.__sessions[token][field] = value

    def __get_session_data(self, token, field):
        print("session contents is")
        print(self.__sessions)
        print("look up token", token)
        #session = self.__sessions.get(token)
        
        print("found session", session)
        if session:
            value = session.get(field)
            return value
        return None

    def run(self, host="0.0.0.0", port=8000):
        self.__app.run(host=host, port=port)



####################################

if __name__ == "__main__":

    server = MathQuizGame()




    server.run()