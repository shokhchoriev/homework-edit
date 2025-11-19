from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "secret-key"
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route("/")
def index():
    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    task_name = request.form.get("task_name")   
    if task_name:
        task = Task(title=task_name)
        db.session.add(task)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)