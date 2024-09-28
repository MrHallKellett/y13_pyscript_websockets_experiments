import asyncio
from js import console
from pyscript import document, when
from pyodide.http import pyfetch
from json import loads
from pyweb import pydom
from random import randint

answer = ""
question_log = []
solved = []
container = pydom["#container"][0]

@when("keypress", "body")
def handle_keypress(key):
    global answer
    print(f"{key.code} was pressed.")
    code = key.code
    if "Enter" in code:
        check_answers()
        answer = ""
    else:
        num = code[-1]
        if num.isdigit():
            answer += num
        else:
            print("invalid digit")

def check_answers():
    for q in question_log:
        if eval(str(q.html)) == int(answer):
            print("Correct!", q.html, "=", answer, "!!!!")
            q.style["color"] = "green"
            q.html += f" = {answer}"
            solved.append(q)
    
    for q in solved:
        try:
            question_log.remove(q)
        except ValueError:
            pass


def add_question_to_page(question):
    x, y, fs = randint(1, 1000), randint(1, 1000), randint(8, 72)
    this_question = container.create("span")
    this_question.style["position"] = f"fixed"
    this_question.style["left"] = f"{x}px"
    this_question.style["top"] = f"{y}px"
    this_question.style["font-size"] = f"{fs}px"        
    this_question.html = question
    question_log.append(this_question)


async def display_questions():

    result = await pyfetch(
        url="/get_new_questions",
        method="GET",
        headers={"Content-Type": "application/json; charset=UTF-8"}
    )

    questions = await result.json()
    console.log("loaded questions")
    
    

    for question in loads(questions):
        console.log(f"found question {question}")
        add_question_to_page(question)
        
        

def fetch_data():
    asyncio.ensure_future(display_questions())



fetch_data()