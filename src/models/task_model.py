from src import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(100))
    body = db.Column(db.String(1000))
    created_at = db.Column(db.DATETIME)
    is_modified = db.Column(db.Boolean)

    def to_json(self):
        created_at_str = self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'body': self.body,
            'created_at': created_at_str,
            'is_modified': self.is_modified
        }
