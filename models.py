from typing import List, Dict

class Question:
    def __init__(self, text: str, correct_answer: int, colour: str):
        self.__text = text
        self.__correct_answer = correct_answer
        self.__answered_by = None  # int, id_ of first player to answer
        self.__colour = colour

class Player:
    def __init__(self, name: str, id_: int, colour: str):
        self.__name = name
        self.__id_ = id_
        self.__colour = colour

class Game:
    def __init__(self, name: str, max_players: int, delay: int):
        self.__questions: List[Question] = []
        self.__delay = delay  # num of seconds before game begins
        self.__name = name
        self.__max_players = max_players
        self.__players: Dict[int, Player] = {}

    def _jsonify(self):               
        pass

    def _check_answer(self, guess: int, player_id: int):
        pass
        