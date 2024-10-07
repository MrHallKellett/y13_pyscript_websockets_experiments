from flask import Flask, jsonify, render_template, session
from flask_cors import CORS
from os import environ
from uuid import uuid4
from json import dumps
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


    @app.route("/")
    def main():
        session['difficulty'] = 10
        colour_index = randrange(0, len(colours))
        session['colour'] = colours.pop(colour_index)
        print("You were assigned", session['colour'])
        return render_template("quiz.html", questions=Markup(questions),
                colour=Markup(dumps(session["colour"])))

    @app.route("/get_new_questions")
    def get_questions():
        n = session['difficulty']
        return dumps(source_questions(n))

    @sock.route('/echo')
    def echo(ws):
        while True:            
            data = ws.receive()
            ws.send(data * 2)
            print(data)

    @app.route("/socket_test")
    def test_socket():
        
        return render_template("test_sockets.html")
    

    return app

####################################

if __name__ == "__main__":
    port = int(environ.get("PORT", 8000))
    app = create_app()
    app.run(host="0.0.0.0", port=port)