from flask.cli import with_appcontext
import click
from .models import User
from . import db

@click.command('reset-weekly-scores')
@with_appcontext
def reset_weekly_scores():
    """Reset all users' weekly scores to 0"""
    try:
        User.query.update({User.weekly_score: 0})
        db.session.commit()
        print("Successfully reset all weekly scores")
    except Exception as e:
        db.session.rollback()
        print(f"Error resetting scores: {e}")

# Register in __init__.py
def init_app(app):
    app.cli.add_command(reset_weekly_scores) 