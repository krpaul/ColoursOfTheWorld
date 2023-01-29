# Copyright (C) 2020-2022 House Gordon Software Company LTD
# All Rights Reserved
# License: Proprietary

from collections import OrderedDict
from sqlalchemy import Index
from root import db

class SchoolYear(db.Model):
    __tablename__ = 'school_years'

    school_year_id = db.Column(db.Integer, primary_key=True)
    year_name = db.Column(db.String, nullable=False, unique=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    def current_year():
        return SchoolYear.query.order_by(SchoolYear.school_year_id.desc()).first()

    def __str__(self):
        return "%s" % (self.year_name)

    def __repr__(self):
        return "SchoolYear(id: %d  name: %s)" % \
            (self.school_year_id,self.year_name)


class SchoolSemester(db.Model):
    """
    A 'semester' here is a half-year period,
    relevant for courses that last only half a year (mostly for Div 4),
    as opposed to classes that go on year-long (for divs k-3).

    NOT to be confused with 'school terms', which are for report-card periods,
    and can overlap and cross over multiple semesters.
    """
    __tablename__ = 'school_semesters'

    school_semester_id = db.Column(db.Integer, primary_key=True)

    school_year_id = db.Column(db.Integer,
                               db.ForeignKey("school_years.school_year_id"),
                               nullable=False,
                               index=True)
    school_year = db.relationship("SchoolYear")

    semester_num = db.Column(db.String, nullable=False,index=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    __table_args__ = (
        # Ensure uniqueness
        db.UniqueConstraint('school_year_id', 'semester_num'),
      )

    def __str__(self):
        return "%s - Semester %s" % (self.school_year.year_name, self.semester_num)

    def __repr__(self):
        return "SchoolSemester(id: %d  year: %s  semester: %s)" % \
            (self.school_semester_id,self.school_year.year_name,self.semester_num)




class SchoolTerm(db.Model):
    """ 'terms' are relavant ONLY as report-card periods.
    NOT to be confused with 'semesters'
    """
    __tablename__ = 'school_terms'

    school_term_id = db.Column(db.Integer, primary_key=True)

    school_year_id = db.Column(db.Integer,
                               db.ForeignKey("school_years.school_year_id"))
    school_year = db.relationship("SchoolYear")

    term_num = db.Column(db.String, nullable=False)

    start_date = db.Column(db.Date, nullable=False)

    # "end_date" is in effect the teachers' dead line date
    end_date = db.Column(db.Date, nullable=False)

    # if 'sent' flag is FALSE - this is TENTATIVE future date
    send_date = db.Column(db.Date, nullable=False)

    locked = db.Column(db.Boolean, nullable=False, default=False)

    # an "end-of-year" report-card term should include previous report-cards from the same year
    end_of_year = db.Column(db.Boolean, nullable=False, default=False)

    sent = db.Column(db.Boolean, nullable=False, default=False)

    review_mode = db.Column(db.Boolean, nullable=False, default=False)

    __table_args__ = (
        # Ensure uniqueness
        db.UniqueConstraint('school_year_id', 'term_num'),
      )

    def __str__(self):
        return "%s - Term %s" % (self.school_year.year_name, self.term_num)

    def __repr__(self):
        return "SchoolTerm(id: %d  year: %s  term: %s)" % \
            (self.school_term_id,self.school_year.year_name,self.term_num)
