import datetime

from flask import Flask, render_template, request, redirect

import data_handler

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="Welcome!")


@app.route("/questions")
def questions_list():
    questions = data_handler.get_all_questions()
    for question in questions:
        question["submission_time"] = datetime.datetime.fromtimestamp(int(question["submission_time"]))
    print(questions)
    return render_template("questions.html", title="Question list!", questions=questions)


@app.route("/question")
def question_answers():
    answers = data_handler.get_answers()
    print(answers)
    return render_template("question.html", title="Question answers!")


@app.route("/add_question", methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        question = request.form['question-text']
        index = len(data_handler.read_questions())
        data_handler.save_question({'id': index, 'text':question})
        return redirect('/')
    return render_template("add_question.html", title="Add question!")

@app.route("/about")
def about():
    return render_template("about.html", title="About!")

if __name__ == "__main__":
    app.run()
