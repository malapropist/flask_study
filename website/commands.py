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

@click.command('delete-user')
@click.argument('user_id', type=int)
@with_appcontext
def delete_user(user_id):
    """Delete a user by their ID"""
    try:
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            print(f"Successfully deleted user with ID {user_id}")
        else:
            print(f"No user found with ID {user_id}")
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting user: {e}")

# Register in __init__.py
def init_app(app):
    app.cli.add_command(reset_weekly_scores)
    app.cli.add_command(delete_user) 