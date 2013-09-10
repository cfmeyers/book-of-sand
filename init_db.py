from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, DateTime, Integer, String, Table, Text, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
from datetime import datetime

Base = declarative_base()

tag_task_maps = Table('tag_task_maps', Base.metadata,
                    Column("tag_id",  Integer, ForeignKey("tags.id")),
                    Column("task_id", Integer, ForeignKey("tasks.id")))

tag_event_maps = Table('tag_event_maps', Base.metadata,
                    Column("tag_id",   Integer, ForeignKey("tags.id")),
                    Column("event_id", Integer, ForeignKey("events.id")))

tag_project_maps = Table('tag_project_maps', Base.metadata,
                    Column("tag_id",   Integer, ForeignKey("tags.id")),
                    Column("project_id", Integer, ForeignKey("projects.id")))


########################################################################
class Tags(Base):
    """"""
    __tablename__ = "tags"

    id      = Column(Integer, primary_key=True)
    name    = Column(String)

    #Mappings
    tasks    = relationship("Tasks",  secondary=tag_task_maps,  backref="tags")
    events   = relationship("Events", secondary=tag_event_maps, backref="tags")
    projects = relationship("Projects",secondary=tag_project_maps, backref="tags")

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
    note = Column(Text)


    project_id =Column(Integer, ForeignKey('projects.id'))
    project = relationship("Projects", backref=backref('events', order_by=id))

    def __init__(self, name):
        """"""
        self.name = name
        self.date = datetime.now()

########################################################################
class Tasks(Base):
    """"""
    __tablename__ = "tasks"

    id             = Column(Integer, primary_key=True)
    name           = Column(String)
    date_assigned  = Column(DateTime)
    date_due       = Column(DateTime)
    date_completed = Column(DateTime)

    project_id =Column(Integer, ForeignKey('projects.id'))
    project = relationship("Projects", backref=backref('tasks', order_by=id))

    def __init__(self, name):
        """"""
        self.name = name
        self.date_assigned = datetime.now()

########################################################################
class Projects(Base):
    """"""
    __tablename__ = "projects"

    id     = Column(Integer, primary_key=True)
    name   = Column(String)
    status = Column(String)
    note   = Column(Text)

    def __init__(self, name):
        """"""
        self.name   = name

########################################################################
# class Persons(Base):
#     """"""
#     __tablename__ = "persons"

#     id   = Column(Integer, primary_key=True)
#     name = Column(String)
#     url  = Column(String)

#     #Tags table Foreign Keys and relationship-------------------------
#     tag_id = Column(Integer, ForeignKey("tags.id"))
#     tag    = relationship("Tags", backref=backref("persons", order_by=id))
#     #-------------------------------------------------------------------

#     #----------------------------------------------------------------------
#     def __init__(self, name):
#         """"""
#         self.name = name

########################################################################
# class Places(Base):
#     """"""
#     __tablename__ = "places"

#     id   = Column(Integer, primary_key=True)
#     name = Column(String)
#     url  = Column(String)

#     #Tags table Foreign Keys and relationship-------------------------
#     tag_id = Column(Integer, ForeignKey("tags.id"))
#     tag   = relationship("Tags", backref=backref("places", order_by=id))
#     #-------------------------------------------------------------------


#     #----------------------------------------------------------------------
#     def __init__(self, name):
#         """"""
#         self.name = name

########################################################################


if __name__ == '__main__':

    engine = create_engine('sqlite:///book_of_sand.db')
    Base.metadata.create_all(engine)
