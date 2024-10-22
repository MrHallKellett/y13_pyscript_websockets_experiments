from flask import Flask, jsonify, render_template, session, request, Response
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

colours = ["red", "blue", "orange", "pink", "yellow"]
questions = dumps(source_questions(10))

def create_app(config=None):
    app = Flask(__name__)
    ##############################
    sock = Sock(app)
    sock.init_app(app)
    ##############################
    app.config.update(dict(DEBUG=True))
    app.secret_key = uuid4().hex
    CORS(app)


    # @app.route("/")
    # def main():
    #     session['difficulty'] = 10
    #     colour_index = randrange(0, len(colours))
    #     session['colour'] = colours.pop(colour_index)
    #     print("You were assigned", session['colour'])
    #     return render_template("quiz.html")

    @app.route("/")
    def menu():
        return render_template("menu.html")

    @app.route("/start_game")
    def get_questions():
        n = session['difficulty']
        data = {"questions":source_questions(n),
                "colour":session['colour']}
        return dumps(data)
    
    
    def set_username(username):
        session['username'] = username
        print("new username is", username)
        return f"Your username has been set to {username}."

    @sock.route('/send')
    def echo(ws):
        while True:            
            data = loads(ws.receive())
            print(data)
            mode = data["mode"]
            msg  = data["message"]
            if mode == 0:       # new username
                response = set_username(msg)                
            elif mode == 1:     # new game
                response = create_new_game(msg)
            elif mode == 2:     # join game
                response = join_game(msg)
            elif mode == 3:     # new answer
                response = check_answer(msg)
            ws.send(response)


    @app.route("/socket_test")
    def test_socket():
        
        return render_template("test_sockets.html")
    

    return app

####################################

if __name__ == "__main__":
    port = int(environ.get("PORT", 8000))
    app = create_app()
    app.run(host="0.0.0.0", port=port)