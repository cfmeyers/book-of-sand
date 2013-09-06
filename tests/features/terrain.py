# from lettuce import world
from lettuce import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *
from init_db import Base, Tags, Tasks, Events


@before.each_feature
def setup(feature):
    world.engine = create_engine('sqlite:///:memory:')
    Session = sessionmaker(bind=world.engine)
    world.session = Session()
    Base.metadata.create_all(world.engine)
    world.db_classes= {"tag":Tags, "task":Tasks, "event":Events}
    world.obj_dict = {}


# @after.each_feature
# def teardown_some_feature(feature):
#     world.engine = create_engine('sqlite:///:memory:')
#     Session = sessionmaker(bind=world.engine)
#     world.session = Session()
#     Base.metadata.create_all(world.engine)