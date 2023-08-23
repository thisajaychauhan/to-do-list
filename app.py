from flask import Flask, render_template, request, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import SQLALCHEMY_DATABASE_URI

app = Flask(__name__)
from datetime import datetime
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class TodoList(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    note = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

@app.route('/')
def index():
    notes = TodoList.query.all()
    app.logger.info(notes)
    return render_template('home.html', notes=notes)

@app.route('/add', methods=['POST'])
def add():
    note = request.form.get('note')
    add_note = TodoList(note=note)
    db.session.add(add_note)
    db.session.commit()
    # flash('note added successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit(note_id):
    note = TodoList.query.get(note_id)
    if request.method == 'POST':
        edit_note = request.form.get('edit_note')
        note.note = edit_note
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', note=note)

@app.route('/delete/<int:note_id>', methods=['POST'])
def delete(note_id):
    note = TodoList.query.get(note_id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
