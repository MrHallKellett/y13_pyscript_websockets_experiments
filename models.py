from typing import List, Dict
from uuid import uuid4
from datetime import datetime

class Question:
    def __init__(self, text: str, correct_answer: int, colour: str):
        self.__text = text
        self.__correct_answer = correct_answer
        self.__answered_by = None  # int, id_ of first player to answer
        self.__colour = colour

class Player:
    def __init__(self, name: str, colour: str):
        self.__name = name
        self.__id_ = uuid4()
        self.__colour = colour

class Game:
    def __init__(self, name: str, max_players: int, delay: int, num_questions: int,
                 owner: str):
        self.__questions: List[Question] = []
        self.__delay = delay  # num of seconds before game begins
        self.__name = name
        self.__max_players = max_players
        self.__players: Dict[int, Player] = {}
        self.__num_questions = num_questions
        self.__owner = owner
        self.__created = datetime.now()

    def _jsonify(self):               
        pass

    def _check_answer(self, guess: int, player_id: int):
        pass

    def get_menu_display(self):
        return f"{self.__name.upper()} by {self.__owner}"
        