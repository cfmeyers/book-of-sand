
from sqlalchemy.orm import sessionmaker
import sqlalchemy
from lettuce import *
from datetime import datetime
from init_db import Base, Tags, Tasks, Events
from nose.tools import assert_raises
import db_utils




@step(r"(empty|non-empty) database")
def an_empty_database(step, db_status):

    if db_status == "empty":
        for cl in world.db_classes.values():
            assert_raises(sqlalchemy.exc.InvalidRequestError, world.session.query(cl).one)

    elif db_status == "non-empty":
        flag = False
        for cl in world.db_classes.values():
            if db_utils.has_rows(world.session, cl):
                flag = True
        assert flag


@step(r'the (.*) table has (some|no) rows')
def test_has_rows(step, obj_class, quantity):
    cl = world.db_classes[obj_class]
    if quantity == "no":
        assert not db_utils.has_rows(world.session, cl)
    else:
        assert db_utils.has_rows(world.session, cl)

@step(r'the (.*) table has (\d+) rows')
def test_has_rows(step, obj_class, num):
    cl = world.db_classes[obj_class]
    assert db_utils.number_of_rows(world.session, cl) == int(num)


@step(r'create a (.*) named "(.*)" and add it to the session')
def create_named_object_of(step, obj_class, name):
    cl = world.db_classes[obj_class]
    new_obj = cl(name)
    world.session.add(new_obj)



@step(r'commit the session')
def commit_the_session(step):
    world.session.commit()

@step(r'the (.*) named "(.*)" is autoassigned an id of (\d+)')
def the_object_is_autoassigned_an_id(step, obj_class, name, id):
    assert world.session.query(world.db_classes[obj_class]).one().id == int(id)

@step(r'a database with a (.*) named "(.*)"')
def a_database_with_an_object_with_name(step, obj_class, name):
    cl = world.db_classes[obj_class]
    assert isinstance(world.session.query(cl).filter(cl.name==name).first(), cl)

@step(r'add the (.*) named "(.*)" to the (.*) named "(.*)"')
def add_object_to_object(step, obj_class_1, name_1, obj_class_2, name_2):
    cl_1 = world.db_classes[obj_class_1]#tag
    obj_1 = world.session.query(cl_1).filter(cl_1.name==name_1).first()#workout
    cl_2 = world.db_classes[obj_class_2]#task
    obj_2 = world.session.query(cl_2).filter(cl_2.name==name_2).first()#do 3 pushups

    if obj_class_1 == "tag":
        obj_2.tags = [obj_1]
    else:
        assert 1==2


@step(r'the (.*) named "(.*)" has a list == \[(.*) named "(.*)"\]')
def check_obj1_has_list_with_item_obj2(step, obj_class_1, name_1, obj_class_2, name_2):

    cl_1 = world.db_classes[obj_class_1]#tag
    obj_1 = world.session.query(cl_1).filter(cl_1.name==name_1).one()#workout
    cl_2 = world.db_classes[obj_class_2]#task
    obj_2 = world.session.query(cl_2).filter(cl_2.name==name_2).one()#do 3 pushups
    if obj_class_1 == "tag":
        assert obj_1.tasks == [obj_2]
    else:
        assert 1==2
