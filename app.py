from distutils.log import debug
from email.policy import default
from urllib import request
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# App configurations and declarations
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Databse 'SQLite'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self) -> str:
        return '<Task %r>' % self.id


# app routes
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_created = request.form['text']
        new_task = Todo(text=task_created)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issuse adding your task !"
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    # deleting the task from the database
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an problem deleting you task !"


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Failed !'
    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
