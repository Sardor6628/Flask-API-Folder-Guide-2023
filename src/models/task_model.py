from src import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(100))
    body = db.Column(db.String(1000))
    created_at = db.Column(db.DATETIME)
    is_modified = db.Column(db.Boolean)
