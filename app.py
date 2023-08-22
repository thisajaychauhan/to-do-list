from flask import Flask, render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(200), nullable=False)
    is_done = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/add', methods=['POST'])
def add():
    note = request.form.get('note')
    add_note = Task(note=note)
    db.session.add(add_note)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)