from sqlalchemy import Index

from root import db
from models.dictable import Dictable
from models.timestamp_mixin import TimestampMixin

class Book(db.Model, Dictable, TimestampMixin):
    __tablename__ = "library_books"

    # essential fields
    id = db.Column(db.Integer, primary_key=True)
    renert_id = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)

    # extra columns that are purely for information tracking
    divisions = db.Column(db.String, nullable=True)
    reading_program = db.Column(db.String, nullable=True)
    notes = db.Column(db.String, nullable=True)
    fp_reading_level = db.Column(db.String, nullable=True)

    transactions = db.relationship("Transaction", backref="book")

    def get_all_ids():
        return [dict(x)['renert_id'] for x in db.session.execute("SELECT DISTINCT RENERT_ID FROM LIBRARY_BOOKS")]

    def __str__(self):
        return f"{self.title} ({self.author})"

    def __repr__(self):
        return f"<Book #{self.renert_id}>"
