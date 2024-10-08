import asyncio
from js import console
from pyscript import document, when
from pyodide.http import pyfetch
from json import loads, dumps
from pyweb import pydom
from random import randint


answer = ""
question_log = []
solved = []
container = pydom["#container"][0]
positions = []
colour = None


###############################################

@when("keypress", "body")
def handle_keypress(key):
    global answer
    print(f"{key.code} was pressed.")
    code = key.code
    negative = False
    if "Enter" in code: # handles both enters on keyboard
        asyncio.ensure_future(check_answer_new(answer))
        answer = ""
    elif "Minus" in code or "Subtract" in code:
        if "-" not in answer:
            answer = "-" + answer
    else:
        char = code[-1]
        if char.isdigit():
            answer += char           
        else:
            print("invalid digit")

###############################################

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

def display_user():
    user = container.create("span")
    user.style["color"] = colour
    user.style["left"] = "300px"
    user.style["top"] = "50px"
    user.style["font-size"] = "72px"
    user.html = "You are logged in."



###############################################

def add_question_to_page(question_num, question):
    # modify this subroutine so questions do not
    # ever overlap
    x, y, fs = randint(1, 1000), randint(1, 1000), randint(8, 72)
    this_question = container.create("span", classes=[f"q{question_num}"])
    
    
    this_question.style["position"] = f"fixed"
    this_question.style["left"] = f"{x}px"
    this_question.style["top"] = f"{y}px"
    this_question.style["font-size"] = f"{fs}px"        
    this_question.html = question
   
    question_log.append(this_question)

###############################################
    

async def check_answer_new(answer):


    print(f"Using pyfetch to send {answer} to server")
    result = await pyfetch(
        url="/check_answer",
        method="POST",
        headers={"Content-Type": "application/json"},
        body = dumps(answer)
    )
    
    data = await result.json()

    print("Received a result", data)
    

async def display_questions():
    global colour
    result = await pyfetch(
        url="/start_game",
        method="GET",
        headers={"Content-Type": "application/json; charset=UTF-8"}
    )

    data = await result.json()
    print("loaded questions")

    server_generated_questions = loads(data['questions'])

    
    colour = data['colour']
    
    print("Here are the questions...")
    print(server_generated_questions)
    print("Here is the colour")
    print(colour)


    display_user()

    for index, question in enumerate(server_generated_questions):
        print(f"found question {question}")
        add_question_to_page(index, question)
      
###############################################
        
def fetch_data():
    asyncio.ensure_future(display_questions())

###############################################

fetch_data()