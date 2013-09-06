
from sqlalchemy.orm import sessionmaker
import sqlalchemy
from lettuce import *
from datetime import datetime
from init_db import Base, Tags, Tasks, Events
from nose.tools import assert_raises

##Generic Steps
@step(r"an empty database")
def an_empty_database(step):
    assert_raises(sqlalchemy.exc.InvalidRequestError, world.session.query(Tasks).one)

@step(r'When I create a (.*) object with a name of "(.*)"')
def create_object_with_name_of(step, obj_class, name):
    cl = world.db_classes[obj_class]
    date_assigned = datetime.now()
    world.obj_dict[name] = cl(name, date_assigned)
    assert isinstance(world.obj_dict[name], cl)

@step(r'And query the database for the (.*) object with name of "(.*)"')
def and_query_the_database_for_the_object(step, obj, name):
    cl = world.db_classes[obj]
    # world.queried_task = world.session.query(cl).filter(cl.name==name).one()
    world.obj_dict[name] = world.session.query(cl).filter(cl.name==name).one()

@step(r'And add the object with a name of "(.*)" to the session')
def and_add_the_object_to_the_session(step, name):
    world.session.add(world.obj_dict[name])

@step(r'And commit the session')
def and_commit_the_session(step):
    world.session.commit()

@step(r'Given a database with a (.*) with name of "(.*)"')
def given_a_database_with_an_object_with_name_of(step, obj_class, name):
    cl = world.db_classes[obj_class]
    world.obj_dict[name] = world.session.query(cl).filter(cl.name==name).first()



@step(r'Then the (.*) object is autoassigned an id of 1')
def then_the_object_is_autoassigned_an_id_of_1(step, obj):
    assert world.session.query(world.db_classes[obj]).one().id == 1

# @step(u'And I create a tag object with a name of (.*)')
# def and_i_create_a_tag_object(step, tagname):
#     world.my_tag = Tags(tagname)

# @step(r'And add the tag to the session')
# def and_add_the_tag_to_the_session(step):
#     world.session.add(world.my_tag)

# @step(r'And query the database for the (.*) object')
# def and_query_the_database_for_the_tag_object(step, obj_class):
#     cl = world.db_classes[obj_class]
#     world.queried_tag = world.session.query(cl).one()

@step(r'Then the (.*) object with a name of "(.*)" is autoassigned an id of 1')
def then_the_object_is_autoassigned_an_id_of_1(step, obj_class, name):
    cl = world.db_classes[obj_class]
    assert world.session.query(cl).filter(cl.name==name).one().id == 1



@step(r'When I add the tag with name of "(.*)" to the task with name of "(.*)"')
def add_tag_to_the_task(step, name_1, name_2):
    world.obj_dict[name_2].tags = [world.obj_dict[name_1]]

@step(u'Then the task object will have a list consisting of the single tag I had added')
def then_the_task_object_will_have_a_list_consisting_of_the_single_tag_i_had_added(step):
    assert world.queried_tag.tasks == [world.queried_task]

@step(u'Then the tag object will have a list consisting of the single task I had added')
def then_the_tag_object_will_have_a_list_consisting_of_the_single_task_i_had_added(step):
    assert world.queried_task.tags == [world.queried_tag]

@step(u'When I create an event object with a name of (.*) and date of today')
def when_i_create_an_event_object_with_a_name_of_baby_wet_her_diaper_and_date_of_today(step, name):
    date_happened = datetime.now()
    world.wetdiaper = Events(name, date_happened)
    assert isinstance(world.wetdiaper, Events)

@step(u'And add the event to the session')
def and_add_the_event_to_the_session(step):
    world.session.add(world.wetdiaper)

@step(u'And I add the tag to the event')
def and_i_add_the_tag_to_the_event(step):
    world.wetdiaper.tags = [world.my_tag]

@step(u'And query the database for the event object')
def and_query_the_database_for_the_event_object(step):
    world.queried_event = world.session.query(Events).one()

@step(u'Then the event object will have a list consisting of the single tag I had added')
def then_the_event_object_will_have_a_list_consisting_of_the_single_tag_i_had_added(step):
    assert world.queried_event.tags == [world.my_tag]
