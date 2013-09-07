from sqlalchemy.orm import sessionmaker
import sqlalchemy
from init_db import *
from datetime import datetime, timedelta


def establish_db_session(path="", db_name="book_of_sand.db"):
    engine  = create_engine('sqlite:///'+path+db_name)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def number_of_rows(session, cl):
    """Returns the number of rows a table has.  If the table has no rows, returns 0.

    Args: session:sqlalchemy session object
          cl:an sqlalchemy table class

    Returns: returns an integer
    """
    return session.query(cl).count()


def has_rows(session, cl):
    """Returns true if table has at least one row, false otherwise

    Args: session:sqlalchemy session object
          cl:an sqlalchemy table class

    Returns: Boolean
    """

    if session.query(cl).first():
        return True
    return False
