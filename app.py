from urllib import request
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    view_number = db.Column(db.Integer, default=1)
    vote_number = db.Column(db.Integer, default=1)
    title = db.Column(db.String(200), nullable=False)
    image_id = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route("/", methods=['POST', 'GET'])
@app.route("/index", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_title = request.form['title']
        task_content = request.form['content']
        new_task = Todo(content=task_content, title=task_title)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route("/questions", methods=['POST', 'GET'])
def table():
    if request.method == 'POST':
        task_title = request.form['title']
        task_content = request.form['content']
        new_task = Todo(content=task_content, title=task_title)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/questions')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('table.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting that task"


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        task.title = request.form['title']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)


# @app.route("/questions")
# def questions_list():
#     questions = data_handler.get_all_questions()
#     for question in questions:
#         question["submission_time"] = datetime.datetime.fromtimestamp(int(question["submission_time"]))
#     print(questions)
#     return render_template("questions.html", title="Question list!", questions=questions)


@app.route("/question/<int:id>", methods=['GET', 'POST'])
def question_answers(id):
    task = Todo.query.get_or_404(id)
    task.view_number += 1
    try:
        db.session.commit()
        return render_template("question.html", task=task)
    except:
        return 'There was an issue!'


@app.route("/vote_up/<int:id>", methods=['GET', 'POST'])
def vote_up(id):
    task = Todo.query.get_or_404(id)
    task.vote_number += 1
    try:
        db.session.commit()
        return render_template("question.html", task=task)
    except:
        return 'There was an issue!'


@app.route("/vote_down/<int:id>", methods=['GET', 'POST'])
def vote_down(id):
    task = Todo.query.get_or_404(id)
    task.vote_number -= 1
    try:
        db.session.commit()
        return render_template("question.html", task=task)
    except:
        return 'There was an issue!'


@app.route("/add_question", methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        task_title = request.form['title']
        task_content = request.form['content']
        new_task = Todo(content=task_content, title=task_title)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        return render_template("add_question.html", title="Add question!")


@app.route("/about")
def about():
    return render_template("about.html", title="About!")

if __name__ == "__main__":
    app.run(debug=True)
