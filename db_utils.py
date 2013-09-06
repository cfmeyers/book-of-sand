from sqlalchemy.orm import sessionmaker
import sqlalchemy
from init_db import *
from datetime import datetime, timedelta


def establish_db_session(path="", db_name="book_of_sand.db"):
    engine  = create_engine('sqlite:///'+path+db_name)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
