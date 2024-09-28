import asyncio
from js import console
from pyodide.http import pyfetch
from json import loads
from pyweb import pydom
from random import randint

questions = []

def add_question_to_page(question):
    x, y, fs = randint(1, 1000), randint(1, 1000), randint(8, 72)
    this_question = container.create("span")
    this_question.style["position"] = f"fixed"
    this_question.style["left"] = f"{x}px"
    this_question.style["top"] = f"{y}px"
    this_question.style["font-size"] = f"{fs}px"        
    this_question.html = question


async def display_questions():

    result = await pyfetch(
        url="/get_new_questions",
        method="GET",
        headers={"Content-Type": "application/json; charset=UTF-8"}
    )

    questions = await result.json()
    console.log("loaded questions")
    container = pydom["#container"][0]
    console.log("selected container")

    for question in loads(questions):
        console.log(f"found question {question}")
        add_question_to_page(question)
        questions.append(question)
        

def fetch_data():
    asyncio.ensure_future(display_questions())



fetch_data()