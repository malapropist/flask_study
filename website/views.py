from flask import Blueprint, render_template, request, flash, jsonify, g
from flask_login import login_user, login_required, logout_user, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == "POST":
        note = request.form.get("note")
        if len(note)<1:
            flash('Enter a note', category='error')
        else:
            flash('Added note to database', category='success')
            new_note = Note(data=note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
    return render_template("home.html", user=current_user)

@views.route('/verses/<int:noteID>', methods=['GET','POST'])
@login_required
def verse_select(noteID):
    # get all notes
    notes_for_user = Note.query.filter(Note.user_id==current_user.id)
    # select single note which user chose
    note_from_id = notes_for_user.filter(Note.id==noteID)
    
    # perform verseus logic on it

    return render_template("select_verse.html", user=current_user,notes=notes)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteID = note['noteId']
    note = Note.query.get(noteID)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})