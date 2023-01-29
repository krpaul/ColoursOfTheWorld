from email.policy import default
from xml.sax import default_parser_list
from sqlalchemy import Index

from root import db
from models.dictable import Dictable
from models.timestamp_mixin import TimestampMixin

import pickle

class LibrarySettings(db.Model, Dictable, TimestampMixin):
    # essential fields
    id = db.Column(db.Integer, primary_key=True)

    settings = db.Column(db.PickleType)

    def default_settings():
        return {
            "grade_staff": "20",
            "grade_k": "3",
            "grade_1": "3",
            "grade_2": "3",
            "grade_3": "3",
            "grade_4": "3",
            "grade_5": "3",
            "grade_6": "3",
            "grade_7": "3",
            "grade_8": "3",
            "grade_9": "3",
            "grade_10": "3",
            "grade_11": "3",
            "grade_12": "3",
        }
    
    def keys():
        return list(LibrarySettings.default_settings().keys())

    # returned current/latest settings
    def latest():
        curr = LibrarySettings.query.order_by(LibrarySettings.updated_at.desc())
        if curr.count() == 1:
            return pickle.loads(curr.first().settings)
        return LibrarySettings.default_settings()

    # update chosen settings
    def update(new_settings):
        filled = dict()
        
        old_settings = LibrarySettings.latest()
        old_settings_keys = old_settings.keys()
        new_settings_keys = new_settings.keys()
        
        # construct new settings dict, using old values for non provided updated keys
        for k in old_settings_keys:
            if k in new_settings_keys:
                filled[k] = new_settings[k]
            else:
                filled[k] = old_settings[k]

        new = LibrarySettings(settings=pickle.dumps(filled))
        
        db.session.add(new)
        db.session.commit()
