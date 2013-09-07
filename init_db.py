from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, DateTime, Integer, String, Table, Text, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
from datetime import datetime

Base = declarative_base()

tag_task_maps = Table('tag_task_maps', Base.metadata,
                    Column("tag_id", Integer, ForeignKey("tags.id")),
                    Column("task_id", Integer, ForeignKey("tasks.id")))

########################################################################
class Tags(Base):
    """"""
    __tablename__ = "tags"

    id   = Column(Integer, primary_key=True)
    name = Column(String)

    tasks = relationship("Tasks", secondary=tag_task_maps, backref="tags")

    #----------------------------------------------------------------------
    def __init__(self, name):
        """"""
        self.name = name

########################################################################
class Events(Base):
    """"""
    __tablename__ = "events"

    id   = Column(Integer, primary_key=True)
    name = Column(String)
    date = Column(DateTime)

    #----------------------------------------------------------------------
    def __init__(self, name):
        """"""
        self.name = name
        self.date = datetime.now()

########################################################################
class Projects(Base):
    """"""
    __tablename__ = "projects"

    id   = Column(Integer, primary_key=True)
    name = Column(String)
    status = Column(String)

    #----------------------------------------------------------------------
    def __init__(self, name, status):
        """"""
        self.name = name
        self.status = status

########################################################################
class Persons(Base):
    """"""
    __tablename__ = "persons"

    id   = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)

    #----------------------------------------------------------------------
    def __init__(self, name):
        """"""
        self.name = name

########################################################################
class Places(Base):
    """"""
    __tablename__ = "places"

    id   = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)

    #----------------------------------------------------------------------
    def __init__(self, name):
        """"""
        self.name = name

########################################################################
class Tasks(Base):
    """"""
    __tablename__ = "tasks"

    id             = Column(Integer, primary_key=True)
    name           = Column(String)
    date_assigned  = Column(DateTime)
    date_due       = Column(DateTime)
    date_completed = Column(DateTime)

    #----------------------------------------------------------------------
    def __init__(self, name):
        """"""
        self.name = name
        self.date_assigned = datetime.now()

########################################################################
if __name__ == '__main__':

    engine = create_engine('sqlite:///book_of_sand.db')
    Base.metadata.create_all(engine)
