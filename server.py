from urllib import request
from flask import Flask, render_template, request, redirect, session
from datetime import datetime
import bcrypt

import utils
import data_handler

app = Flask(__name__)
app.secret_key = 'xd2137xd1045xd420'

@app.route("/")
@app.route("/index")
@app.route("/index/<int:limit>")
def index(limit=3):
    # if not is_loggedin():
    #     return redirect('/login')
    if request.method == 'POST':
        questions = data_handler.get_top_questions(str(limit))
        questions = utils.to_datetime(questions)
        return render_template('index.html', questions=questions, limit=limit, title="Hello!")
    questions = data_handler.get_top_questions(str(limit))
    questions = utils.to_datetime(questions)
    return render_template('index.html', questions=questions, limit=limit, title="Hello!")


def is_loggedin():
    return 'user_email' in session


def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_email = request.form['email']
        user_password = request.form['password']
        user_credentials_from_db = data_handler.get_user(user_email)
        hashed_password = user_credentials_from_db[0]['user_password']
        if verify_password(user_password, hashed_password):
            session["user_email"] = user_email
            return redirect('/index')
        else:
            return render_template('login.html', titel="Login!", message='Wrong password!')
    return render_template('login.html', titel="Login!")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_name = request.form['name']
        user_email = request.form['email']
        user_password = request.form['password']
        hashed_password = hash_password(user_password)
        user = {'user_name': user_name, 'user_email': user_email, 'user_password': hashed_password}
        data_handler.add_user(user)
        return redirect('/index')
    return render_template('register.html', titel="Register!")


@app.route("/questions", methods=['POST', 'GET'])
def questions():
    if not is_loggedin():
        return redirect('/login')
    questions = utils.to_datetime(data_handler.get_all_questions())
    return render_template('questions.html', questions=questions, title="All Questions")


@app.route('/delete/<int:id>')
def delete(id):
    if not is_loggedin():
        return redirect('/login')
    data_handler.delete_row(id)
    return redirect('/table')


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if not is_loggedin():
        return redirect('/login')
    if request.method == 'POST':
        question_content = request.form['content']
        question_title = request.form['title']
        data_handler.alter_row(id, "content", question_content)
        data_handler.alter_row(id, "title", question_title)
        return redirect('/questions')
    question = data_handler.read_question(id)
    return render_template("update.html", questions=question, title="Update!")


@app.route("/table")
def questions_table():
    if not is_loggedin():
        return redirect('/login')
    questions = data_handler.get_all_questions()
    return render_template("table.html", questions=questions, title="Production table!")


@app.route("/question/<int:id>", methods=['GET', 'POST'])
def question_views(id):
    if not is_loggedin():
        return redirect('/login')
    question = utils.to_datetime(data_handler.read_question(id))
    if question[0]['view_number'] is None:
        question[0]['view_number'] = 1
    else:
        question[0]['view_number'] += 1
    data_handler.alter_row(id, "view_number", question[0]['view_number'])
    return render_template("question.html", questions=question)


@app.route("/vote_up/<int:id>", methods=['GET', 'POST'])
def vote_up(id):
    if not is_loggedin():
        return redirect('/login')
    task = data_handler.read_question(id)
    print(task)
    if task[0]["vote_number"] is None:
        task[0]["vote_number"] = 1
    else:
        task[0]["vote_number"] += 1
    data_handler.alter_row(id, "vote_number", task[0]["vote_number"])
    return render_template("question.html", questions=task)


@app.route("/vote_down/<int:id>", methods=['GET', 'POST'])
def vote_down(id):
    if not is_loggedin():
        return redirect('/login')
    task = data_handler.read_question(id)
    print(task)
    if task[0]["vote_number"] is None:
        task[0]["vote_number"] = -1
    else:
        task[0]["vote_number"] -= 1
    data_handler.alter_row(id, "vote_number", task[0]["vote_number"])
    return render_template("question.html", questions=task)


@app.route("/add_question", methods=['GET', 'POST'])
def add_question():
    if not is_loggedin():
        return redirect('/login')
    if request.method == 'POST':
        question_title = request.form['title']
        question_content = request.form['content']
        question_author = request.form['author']
        question_date = int(datetime.timestamp(datetime.now()))
        new_question = {'content': question_content, 'title': question_title,
                        'date_created': question_date}
        try:
            data_handler.save_question(new_question)
            return redirect('/questions')
        except:
            return 'There was an issue adding your task'
    return render_template("add_question.html", title="Add question!")


@app.route('/add_answer', methods=["POST"])
def add_answer():
    if not is_loggedin():
        return redirect('/login')
    if request.method == 'POST':
        answer_content = request.form['content']
        answer = {'content': answer_content}
        try:
            data_handler.save_answer(answer)
            return redirect('/question')
        except:
            return 'There was an issue adding your task'
    return render_template("add_answer.html", title="Add answer!")


@app.route("/about")
def about():
    # if not is_loggedin():
    #     return redirect('/login')
    return render_template("about.html", title="About!")


if __name__ == "__main__":
    app.run(debug=True)
