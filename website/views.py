from flask import Blueprint, render_template, request, flash, jsonify, g, send_from_directory, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from .models import Note
from . import db
from .verseus import Verse_Test
import json

views = Blueprint('views', __name__)

@views.route('/')
def landing():
    return render_template("landing.html", user=current_user)

@views.route('/home', methods=['GET'])
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
    return render_template("home.html", user=current_user, books=books_of_the_bible)

@views.route('/verses', methods=['GET'])
@login_required
def verses():
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
    return render_template("verses.html", user=current_user, books=books_of_the_bible)

@views.route('/add-note', methods=['GET', 'POST'])
@login_required
def add_note():
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
        title = request.form.get("title")
        # TODO reevaluate this
        if len(note) < 1:
            flash('Please enter note content', category='error')
        elif len(title) < 1:
            flash('Please enter a title', category='error')
        else:
            new_note = Note(title=title, data=note, user_id=current_user.id, ref=ref)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added successfully!', category='success')
            return redirect(url_for('views.home'))
            
    return render_template("add_note.html", user=current_user, books=books_of_the_bible)

@views.route('/verses/<int:note_id>', methods=['GET', 'POST'])
@login_required
def practice_verse(note_id):
    verse_test = Verse_Test(current_user=current_user, note_id=note_id)

    if not verse_test.verse:
        flash('Verse not found', category='error')
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        user_answer = request.form.get('answer')
        current_score, potential_score, message = verse_test.check_answer(user_answer)

        result = {
            'current_score': current_score,
            'potential_score': potential_score,
            'message': message
        }
        
        return render_template("practice_verse.html", 
                             verse_info=verse_test.get_verse_info(),
                             result=result,
                             note_id=note_id, user=current_user)
    
    return render_template("practice_verse.html", 
                         verse_info=verse_test.get_verse_info(),
                         note_id=note_id, user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteID = note['noteId']
    note = Note.query.get(noteID)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            # return redirect(url_for('views.verses'))

    return jsonify({})

