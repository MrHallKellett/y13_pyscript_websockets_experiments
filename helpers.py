from random import randint, choice
from typing import List
from json import dumps

OPERATORS = "*+-"

def generate_math_question() -> str:
    return f"{randint(1, 10)} {choice(OPERATORS)} {randint(1, 10)}"

def source_questions(n: int) -> str:
    return dumps([generate_math_question() for _ in range(n)])