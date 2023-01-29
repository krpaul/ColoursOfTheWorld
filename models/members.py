# Copyright (C) 2020-2022 House Gordon Software Company LTD
# All Rights Reserved
# License: Proprietary

from flask_login import UserMixin
from sqlalchemy import Index
from pprint import pprint

from root import db
from models.dictable import Dictable
from models.login_users import LoginUser
from models.photos import Photo

"""
To load from TSV:

  \copy members(last_name,first_name,grade,school_id,online) from 'students2.tsv';                                                          
  COPY 627

"""

class Member(UserMixin, db.Model, Dictable):
    __tablename__ = 'members'

    member_internal_id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, nullable=False, unique=True)
    last_name = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String,nullable=False)
    nickname = db.Column(db.String)

    grade = db.Column(db.Enum('1',
                              '2',
                              '3',
                              '4',
                              '5',
                              '6',
                              '7',
                              '8',
                              '9',
                              '10',
                              '11',
                              '12',
                              'K',
                              'Staff',
                              'JK',
                              'Volunteers',
                              name='member_grade'),
                      nullable=False)

    online = db.Column(db.Boolean,nullable=False,default=False)

    transactions = db.relationship("Transaction", backref="member")

    login_user_id = db.Column(db.Integer,
                                  db.ForeignKey("login_users.login_user_id"))

    active = db.Column(db.Boolean,nullable=False,default=True)

    # Global/Alberta Student ID ?
    school_udid = db.Column(db.Integer, unique=True)

    pronoun = db.Column(db.Enum('M',
                              'F',
                              'T',
                              name='pronouns'),
                        nullable=True)

    login_user = db.relationship("LoginUser", backref="member", uselist=False)

    photos = db.relationship("Photo", order_by='desc(Photo.year)')

    def __init__(self):
        pass

    @property
    def id(self):
        return self.member_internal_id

    def get_id(self):
        return self.member_internal_id

    @property
    def division(self):
        g = self.grade
        if g == 'K':
            return 'K'
        elif g in ['1','2','3']:
            return '1'
        elif g in ['4','5','6']:
            return '2'
        elif g in ['7','8','9']:
            return '3'
        elif g in ['10','11','12']:
            return '4'
        else:
            raise RuntimeError("should not happen")

    @property
    def is_active_student(self):
        # NOTE: "JK" is not considered part of the school (yet)
        return self.active and self.grade in ['K','1','2','3','4','5','6','7','8','9','10','11','12']

    @property
    def is_staff(self):
        return self.grade == "Staff"

    @property
    def is_volunteer(self):
        return self.grade == "Volunteers"

    @property
    def display_name(self):
        s = self.first_name
        if self.nickname:
            s += " (" + self.nickname + ")"
        s += " " + self.last_name
        return s

    @property
    def common_name(self):
        if self.nickname:
            return self.nickname
        return self.first_name

    @property
    def reverse_display_name(self):
        s = self.last_name + ", " + self.first_name
        if self.nickname:
            s += " (" + self.nickname + ")"
        return s


    @property
    def abbr_name(self):
        return self.first_name + " " + \
               self.last_name[0] + "."

    @property
    def display_name_grade(self):
        s = self.last_name + ", " + self.first_name + " "
        if self.nickname:
            s += "(" + self.nickname + ") "
        if self.is_staff:
            s += "(Staff)"
        elif self.is_volunteer:
            s += "(Volunteer)"
        else:
            s += "(Gr. " + self.grade + ")"
        return s

    @property
    def latest_photo(self):
        l = list(self.photos)
        if len(l)==0:
            return None
        return l[0]

    def get_signed_out_books(self):
        pass

    def get_homeroom(self, school_year_id):
        h = [c for c in self.class_instances \
             if ( (c.school_year_id==school_year_id) and (c.class_definition.category == 'Homeroom') )]
        if len(h)==0:
            return None
        if len(h)>1:
            return ValueError("DB consistency error: student-member-id %s has more than one homeroom class in school_year_id %s" \
                              % ( self.member_internal_id, school_year_id ) )
        return h[0]


    def compile_comment(self,comment):
        c = str(comment)
        nick = self.nickname if self.nickname else self.first_name

        ## NOTE: Placeholders DO NOT support "possessive pronouns" e.g.:
        ##   Hers/His/Theirs
        if self.pronoun == 'M':
            he_she = 'he'
            capital_he_she = 'He'

            him_her = 'him'
            capital_him_her = 'Him'

            his_her = 'his'
            capital_his_her = 'His'
        elif self.pronoun == 'F':
            he_she = 'she'
            capital_he_she = 'She'

            him_her = 'her'
            capital_him_her = 'Her'

            his_her = 'her'
            capital_his_her = 'Her'
        elif self.pronoun == 'T':
            he_she = 'they'
            capital_he_she = 'They'

            him_her = 'them'
            capital_him_her = 'Them'

            his_her = 'Their'
            capital_his_her = 'Their'
        else:
            raise RuntimeError("Not implemented Yet")

        c = re.sub("\[ *(Jonathan|Johnathan) *\]",self.first_name, c,re.IGNORECASE)
        c = re.sub("\[ *(John|Johnny|Johnnie|Johnie|Johny|Johni) *\]",nick, c, flags=re.IGNORECASE)

        c = re.sub("\[ *(he) *\]", he_she , c)
        c = re.sub("\[ *(He) *\]", capital_he_she , c)

        c = re.sub("\[ *(him) *\]", him_her , c)
        c = re.sub("\[ *(Him) *\]", capital_him_her , c)

        c = re.sub("\[ *(his) *\]", his_her , c)
        c = re.sub("\[ *(His) *\]", capital_his_her , c)

        return c;


    def __str__(self):
        return self.display_name_grade

    def __repr__(self):
        return "Member(internal-id: %d  school-id: %d  name: %s %s)" % \
            (self.member_internal_id,self.school_id,self.first_name,self.last_name)

Index("members_school_id", Member.school_id)
Index("members.last_name", Member.last_name)
Index("members.first_name", Member.first_name)
Index("members.grade", Member.grade)
Index("members.online", Member.online)


import re
from sqla_quote_literal import quote_literal

def resolve_students_by_name(multiline_string_of_names,
                            return_dict=False):
    students = multiline_string_of_names

    students = [x.lower().strip().replace("*","") for x in students.split("\n")] # chomp
    students = [x for x in students if x] # remove empty lines
    students = [re.sub("\s*\([^)]*\)\s*","",x) for x in students] # remove any words in parenthesis

    orig_students = students # save for later

    #Convert any unicode single-quote variant to sane ascii
    #NOTE: the ASCII single-quote will be psql-quoted below for SQL safety.
    students = [x.replace("\u2019","'").replace("`","'").replace("\u00B4","'").replace("\u2018","'").strip() for x in students]

    def split_student_name(s):
        if s.count(",")==1:
            # Assume the comma splits the first,last parts
            parts = [x.strip() for x in re.split(",",s)]
            return parts
        else:
            # Split by spaces, limit to 2 parts
            # (e.g. so "John Von Doe" becomes "John","Von Doe")
            parts = [x.strip() for x in re.split(" +",s,2)]
            return parts

    # Split into last,first names
    students = [split_student_name(x) for x in students]

    # If any name part contains a dash or space (e.g. "Foo-Bar" and "Baz Van Zant") -
    # keep only the first part
    students = [ [re.sub("[- ]+.*$","",y) for y in x] for x in students]


    sql_values = [ "(%d,unaccent(%s),unaccent(%s))" % (i, quote_literal(db,x[0]), quote_literal(db,x[1])) for i,x in enumerate(students) ]

    names_cte_sql = "with names(dummyid,name1,name2) as ( values " + \
        ",\n".join(sql_values) + ")"

    sql = names_cte_sql + """
          select *
          from
             names
          left join
             members
          on
              -- name1 is first/nick, name2 is last
              (
                ((lower(unaccent(first_name)) = name1) or (lower(unaccent(nickname)) = name1))
                and
                (lower(unaccent(last_name)) ilike (name2 || '%'))
              )
              or
              -- name2 is first/nick, name1 is last
              (
                ((lower(unaccent(first_name)) = name2) or (lower(unaccent(nickname)) = name2))
                and
                (lower(unaccent(last_name)) ilike (name1 ||'%'))
              )
          where
             members.active
            or
             members.member_internal_id is null
          order by
             dummyid
          """

    rc = db.session.execute(sql)
    rc = [dict(x) for x in rc]

    found = [x for x in rc if x.get('member_internal_id',None)]
    not_found = [x for x in rc if not x.get('member_internal_id',None)]

    # Remove the superfluous fields (used for the join)
    for x in found:
        x.pop("dummyid",None)
        x.pop("name1",None)
        x.pop("name2",None)

    if not return_dict:
        # Instead of returning a raw dictionary of result,
        # Load a Member object for each result.
        #
        # (will execute a somewhat duplicated SQL query to the above, not ideal, but not too bad)
        found_ids = [ x['member_internal_id'] for x in found ]
        found = db.session.query(Member).filter(Member.member_internal_id.in_(found_ids)).all()


    # Get the original names as provided by the caller, before any manipulation
    # 'dummyid' is their index in the input list
    not_found = [ orig_students[ x['dummyid'] ] for x in not_found ]


    return (found, not_found)
