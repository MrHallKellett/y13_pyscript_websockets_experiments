import os

from flask import Flask, jsonify, render_template, session
from flask_cors import CORS
from helpers import source_questions
from uuid import uuid4
from json import dumps

def create_app(config=None):
    app = Flask(__name__)
    app.config.update(dict(DEBUG=True))
    app.secret_key = uuid4().hex
    CORS(app)

    

    @app.route("/")
    def main():
        session['difficulty'] = 10
        return render_template("quiz.html")

    @app.route("/get_new_questions")
    def get_questions():
        n = session['difficulty']
        return dumps(source_questions(n))

    return app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app = create_app()
    app.run(host="0.0.0.0", port=port)