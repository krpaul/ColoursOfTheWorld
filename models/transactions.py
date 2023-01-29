from root import db
from models.dictable import Dictable
from datetime import datetime as dt, timedelta
from sqlalchemy import and_
from models.timestamp_mixin import TimestampMixin

class Transaction(db.Model, Dictable, TimestampMixin):
    OVERDUE_PERIOD_DAYS = 14
    __tablename__ = "library_transactions"

    id = db.Column(db.Integer, primary_key=True)
    returned = db.Column(db.Boolean, nullable=False, default=False)
    
    # foreign key for book
    book_id = db.Column(db.Integer, db.ForeignKey('library_books.id'), nullable=False)

    # foreign key for student
    member_id = db.Column(db.Integer, db.ForeignKey("members.member_internal_id"), nullable=False)

    def __init__(self, **kwargs):
        super(Transaction, self).__init__(**kwargs)

        # We have to manually set the ID since postgresql doesn't autoincrement imported rows (https://stackoverflow.com/a/41916342/9628054)
        # self.id = Transaction.query.order_by(Transaction.id.desc()).first().id + 1 


    # returns query of all overdue transactions
    def overdue():
        return db.session.query(Transaction).filter(
            and_(Transaction.returned == False, Transaction.created_at <= dt.utcnow() - timedelta(days=Transaction.OVERDUE_PERIOD_DAYS))
        )

    def homeroom_overdue_with_days(hr):
        overdues = [trans for trans in Transaction.overdue() if trans.student.homeroom == hr]
        days = map(
            lambda trans: int(((dt.utcnow() - timedelta(Transaction.OVERDUE_PERIOD_DAYS)) - trans.created_at).days),
            overdues
        )
        overdues = [trans.to_nested_dict() for trans in overdues]
        
        return list(zip(overdues, days))

    # because JINJA doesn't allow me to access nested db models i have to embed them as dict's I HATE JINJA AND FLASK THIS WOULD HAVE BEEN FINE IN RUBY
    def to_nested_dict(self):
        t_dict = self.toDict()

        # can't import student or book models bc it would cause a circular import
        t_dict['student'] = [dict(r) for r in db.session.execute(f"SELECT * FROM LIBRARY_STUDENTS WHERE ID = {t_dict['student_id']}")][0]
        t_dict['book'] = [dict(r) for r in db.session.execute(f"SELECT * FROM LIBRARY_BOOKS WHERE ID = {t_dict['book_id']}")][0]

        return t_dict
