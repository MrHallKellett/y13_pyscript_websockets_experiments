function randint(start, stop)
{
    return parseInt((Math.random() * stop-start) + stop)
}

function generate_math_question()
{
    return `${randint(1, 10)} ${choice(OPERATORS)} ${randint(1, 10)}`
}

questions

function place_questions(questions)
{
    const body = document.getElementsByTagName("body")[0]
    for (const q of questions)
    {
        let this_q = document.createElement("span")
        this_q.style.position = "fixed"
        this_q.style.left = randint(0, 1000)
        this_q.style.top = randint(0, 1000)

    }
}