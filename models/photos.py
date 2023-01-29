# Copyright (C) 2020-2022 House Gordon Software Company LTD
# All Rights Reserved
# License: Proprietary

from flask_login import UserMixin
from sqlalchemy import Index

from root import db
from models.dictable import Dictable


class Photo(db.Model,Dictable):
    __tablename__ = 'photos'

    photo_id = db.Column(db.Integer, primary_key=True)

    member_id = db.Column(db.Integer,
                          db.ForeignKey("members.member_internal_id"),
                          nullable=False)
    filename = db.Column(db.String)
    source = db.Column(db.String)
    year = db.Column(db.Integer)

    member = db.relationship("Member")

    def __init__(self):
        pass

    def __str__(self):
        return self.display_name_grade

    def __repr__(self):
        return "Photos(photo-id: %d  member-id: %d  filename: %s)" % \
            (self.photo_id, self.member_id,self.filename)
