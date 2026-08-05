from datetime import datetime
from extensions import db


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50))
    isbn = db.Column(db.String(20), unique=True)
    total_copies = db.Column(db.Integer, default=1)
    available_copies = db.Column(db.Integer, default=1)
    added_on = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert the model instance into a JSON-serializable dict."""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "isbn": self.isbn,
            "total_copies": self.total_copies,
            "available_copies": self.available_copies,
            "added_on": self.added_on.isoformat() if self.added_on else None,
        }
