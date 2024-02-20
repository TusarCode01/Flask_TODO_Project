from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(200), nullable=False)

@app.route('/')
def index():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)

@app.route('/submit', methods=['POST','GET'])
def submit():
    if request.method=='POST':
        new_todo = Todo(desc=request.form['todo_text'])
        db.session.add(new_todo)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:sno>',methods=['POST','GET'])
def update(sno):
    if request.method == 'POST':
        todo_text= request.form['todo_text']
        todo = Todo.query.filter_by(sno=sno).first()
        # todo = Todo(desc=request.form['todo_text'])
        todo.desc=todo_text
        # db.session.add(todo)  each time it add new todo
        db.session.commit()
        return redirect (url_for('index'))
    
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)


if __name__ == "__main__":
    app.run(debug=True)