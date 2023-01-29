# Copyright (C) 2020-2022 House Gordon Software Company LTD
# All Rights Reserved
# License: Proprietary

from sqlalchemy import event, DDL
from sqlalchemy import Column, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.schema import MetaData
from sqlalchemy_utils import get_class_by_table
from pprint import pprint
from root import db
from datetime import datetime

"""
Use the following template code to add an 'updated_at' column
and add a trigger that would update the column whenever the
table is updated:

   from psql_update_timestamp_trigger import register_update_timestamp_trigger

   class Data(db.Model):
        ...
        updated_at = db.Column(db.TIMESTAMP(timezone=True),server_default=func.now(), nullable=False)
        ...

   register_update_timestamp_trigger(Data)



see:
https://docs.sqlalchemy.org/en/14/core/ddl.html
https://stackoverflow.com/questions/8929738/sqlalchemy-declarative-defining-triggers-and-indexes-postgres-9
"""


update_timestamp_func_DDL = DDL(
    """
    CREATE OR REPLACE FUNCTION trigger_update_timestamp()
    RETURNS TRIGGER AS $$
    BEGIN
      NEW.updated_at := current_timestamp;
      RETURN NEW;
    END; $$ LANGUAGE PLPGSQL
"""
)
event.listen(MetaData, 'before_create', update_timestamp_func_DDL)




def register_update_timestamp_trigger(table_class):
    table_name = str(table_class.__table__)

    trigger = DDL(
        "CREATE TRIGGER " + table_name + "_update_timestamp BEFORE INSERT OR UPDATE ON " + table_name +
        " FOR EACH ROW EXECUTE PROCEDURE trigger_update_timestamp();"
    )

    event.listen(
        table_class.__table__,
        'after_create',
        trigger.execute_if(dialect='postgresql')
    )


class TimestampMixin():
    """
    COLUMN._creation_order:
       a beautiful hack to ensure the mixin's db.columns
       are created at the end (i.e. AFTER the db.columns of the class
       implementing the mixin).
       see: https://stackoverflow.com/a/3924814

    """
    created_at = Column(TIMESTAMP(timezone=True),server_default=func.now(), default=datetime.utcnow, nullable=False)
    created_at._creation_order = 8001

    updated_at = Column(TIMESTAMP(timezone=True),server_default=func.now(), default=datetime.utcnow, nullable=False)
    updated_at._creation_order = 8002



def foofoo(target, connection, **kw):
    created_tables = kw['tables']
    for tbl in created_tables:
        cls = get_class_by_table(db.Model,tbl)
        if issubclass(cls,TimestampMixin):
            register_update_timestamp_trigger(cls)

event.listen(MetaData,'before_create', foofoo, propagate=True)
