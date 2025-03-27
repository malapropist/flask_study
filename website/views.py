from flask import Blueprint, render_template, request, flash, jsonify, g, send_from_directory
from flask_login import login_user, login_required, logout_user, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    books_of_the_bible = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
    "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
    "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra",
    "Nehemiah", "Esther", "Job", "Psalms", "Proverbs",
    "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah", "Lamentations",
    "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
    "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk",
    "Zephaniah", "Haggai", "Zechariah", "Malachi",
    "Matthew", "Mark", "Luke", "John", "Acts",
    "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians",
    "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians", "1 Timothy",
    "2 Timothy", "Titus", "Philemon", "Hebrews", "James",
    "1 Peter", "2 Peter", "1 John", "2 John", "3 John",
    "Jude", "Revelation"]
    if request.method == "POST":
        note = request.form.get("note")
        ref = request.form.get("chapter_verse")
        
        if len(note)<1:
            flash('Enter a note', category='error')
        else:
            flash('Added note to database', category='success')
            new_note = Note(data=note, user_id = current_user.id, ref=ref)
            db.session.add(new_note)
            db.session.commit()
    return render_template("home.html", user=current_user, books=books_of_the_bible)


@views.route('/verses/<int:noteID>', methods=['GET','POST'])
@login_required
def verse_select(noteID):
    from . import verseus
    # get all notes
    notes_for_user = Note.query.filter(Note.user_id==current_user.id)
    # select single note which user chose
    note_from_id = notes_for_user.filter(Note.id==noteID).all()[0]
    # perform verseus logic on it
    t = verseus.Verse_Test(note_from_id.data, note_from_id.ref)
    u=t.verse
    v=t.reference

    return render_template("select_verse.html", user=current_user,notes=u,ref=v)

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

