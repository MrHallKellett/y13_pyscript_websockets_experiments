from typing import List, Dict
from markupsafe import Markup
from uuid import uuid4
from datetime import datetime
from random import randint, choice
from typing import List
from json import dumps
from config import *
    
class Question:
    def __init__(self, text: str, correct_answer: int):
        self.__text = f"{randint(1, 10)} {choice(OPERATORS)} {randint(1, 10)}"
        self.__correct_answer = eval(self.__text)
        self.__answered_by = None  # int, id_ of first player to answer
        self.__colour = "black"

    def check_answer(self, guess, guesser):
        if guess == self.__correct_answer:
            self.__answered_by = guesser.get_id()
            self.__colour = guesser.get_colour()


    def get_display(self):
        return Markup(f'<span style="color: {self.__colour}">self.__text)

class Player:
    def __init__(self, name: str, colour: str, colours: list):
        self.__name = name
        self.__id_ = uuid4().int
        rand_index = randrange(0, len(colours))
        chosen_colour = colours.pop(rand_index)
        self.__colour = chosen_colour

class Game:
    def __init__(self, name: str, max_players: int, delay: int, num_questions: int,
                 owner: str):
        self.__available_colours = list(COLOURS)
        self.__questions: List[Question] = []
        self.__delay = delay  # num of seconds before game begins
        self.__name = name
        self.__max_players = max_players
        self.__players: Dict[int, Player] = {}
        self.__num_questions = num_questions
        self.__owner = owner
        self.__created = datetime.now()
        self.__id = uuid4().int

    def _jsonify(self):               
        pass

    def _check_answer(self, guess: int, player_id: int):
        pass

    def get_menu_display(self):
        return f"{self.__name.upper()} by {self.__owner}"
        
    def get_id(self):
        return self.__id
    
    def get_secs_til_start(self):
        return (datetime.now() - self.__created).seconds
    
    def get_question_display(self):
        return [question.get_display() for question in self.__questions]
