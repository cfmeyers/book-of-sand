import sys
sys.path.append("utils/")

from sqlalchemy.orm import sessionmaker
import sqlalchemy
from lettuce import *
from datetime import datetime
from nose.tools import assert_raises
import db_utils
import task_script, tag_script
from init_db import Tasks, Tags

##Database Steps
@step(r"(empty|non-empty) database")
def an_empty_database(step, db_status):

    if db_status == "empty":
        for tbl in world.db_classes.values():
            assert_raises(sqlalchemy.exc.InvalidRequestError, world.session.query(tbl.cl).one)

    elif db_status == "non-empty":
        flag = False
        for tbl in world.db_classes.values():
            if db_utils.has_rows(world.session, tbl.cl):
                flag = True
        assert flag


@step(r"a database with <(\d)> <(.*)> objects")
def a_database_with_n_objects(step, num, class_name):
    num = int(num)
    cl = world.db_classes[class_name].cl
    assert world.session.query(cl).count() == num

@step(r'the (.*) table has (some|no) rows')
def test_has_rows(step, class_name, quantity):
    cl = world.db_classes[class_name].cl
    if quantity == "no":
        assert not db_utils.has_rows(world.session, cl)
    else:
        assert db_utils.has_rows(world.session, cl)

@step(r'the (.*) table has (\d+) rows')
def test_has_rows(step, class_name, num):
    cl = world.db_classes[class_name].cl
    assert db_utils.number_of_rows(world.session, cl) == int(num)


@step(r'create a <(.*)> named "(.*)" and add it to the session')
def create_named_object_of(step, class_name, name):
    cl = world.db_classes[class_name].cl
    new_obj = cl(name)
    world.session.add(new_obj)



@step(r'commit the session')
def commit_the_session(step):
    world.session.commit()

@step(r'the (.*) named "(.*)" is autoassigned an id of (\d+)')
def the_object_is_autoassigned_an_id(step, class_name, name, id):
    assert world.session.query(world.db_classes[class_name].cl).first().id == int(id)

@step(r'a database with a (.*) named "(.*)"')
def a_database_with_an_object_with_name(step, class_name, name):
    cl = world.db_classes[class_name].cl
    assert isinstance(world.session.query(cl).filter(cl.name==name).first(), cl)

@step(r'add the <(.*)> named "(.*)" to the <(.*)> named "(.*)"')
def add_object_to_object(step, class_name1, name1, class_name2, name2):

    tbl_1, tbl_2, object_1, object_2 = parse_2_objs_2_names(class_name1, name1, class_name2, name2)

    ##Use the tbl.collection string to get a list from the object
    class_1s_in_object_2 = getattr(object_2, tbl_1.collection)#e.g. sometask.tags = [sometag]
    class_1s_in_object_2.append(object_1)


@step(r'the <(.*)> named "(.*)" has a many-to-many relationship with the <(.*)> named "(.*)"')
def check_many_to_many_relationship(step, class_name1, name1, class_name2, name2):

    tbl_1, tbl_2, object_1, object_2 = parse_2_objs_2_names(class_name1, name1, class_name2, name2)

    ##Use the tbl.collection string to get a list from the object
    class_1s_in_object_2 = getattr(object_2, tbl_1.collection)#e.g. sometask.tags = [sometag]
    class_2s_in_object_1 = getattr(object_1, tbl_2.collection)#e.g. sometag.tasks = [sometask]

    assert object_1 in class_1s_in_object_2
    assert object_2 in class_2s_in_object_1

@step(r'the <(.*)> named "(.*)" has a one-to-many relationship with the <(.*)> named "(.*)"')
def check_one_to_many_relationship(step, class_name1, name_one, class_name_many, name_many):

    one_tuple, many_tuple, one, many = parse_2_objs_2_names(class_name1, name_one, class_name_many, name_many)

    manys_in_one = getattr(one, many_tuple.collection)
    assert many in manys_in_one

    one_in_many = getattr(many, one_tuple.scalar)
    assert one is one_in_many


def parse_2_objs_2_names(class_name1, name1, class_name2, name2):
    ##Named Tuples for each kind of object
    tbl_1 = world.db_classes[class_name1] #e.g. tbl_1.cl == Tag, tbl_1.collection = "tags"
    tbl_2 = world.db_classes[class_name2] #e.g. tbl_2.cl == Task, tbl_2.collection = "tasks"

    ##Class for each kind of object
    class_1 = tbl_1.cl#e.g. Tag
    class_2 = tbl_2.cl#e.g. Task

    ##Objects--find the objects in the db that correspond to the names given
    object_1 = world.session.query(class_1).filter(class_1.name==name1).first()
    object_2 = world.session.query(class_2).filter(class_2.name==name2).first()

    return (tbl_1, tbl_2, object_1, object_2)


#######################task_script steps#######################

@step(r'call create_task with the name "(.*)"')
def check_create_task_with_add_task(step, task_name):
    task = task_script.create_task(world.session, task_name)
    world.session.add(task)

@step(r'create <task> "(.*)" with tags "(.*)", "(.*)", add task to session')
def check_create_task_with_args(step, task_name, tag_name1, tag_name2):
    task = task_script.create_task(world.session, task_name, tag_names=[tag_name1, tag_name2])
    world.session.add(task)

@step(r'the <(.*)> "(.*)" has <(.*)> "(.*)"')
def check_obj1_has_obj2(step, class_name1, name_obj1, class_name2, name_obj2):

    cl1 = world.db_classes[class_name1].cl
    cl2 = world.db_classes[class_name2].cl


    obj1 = world.session.query(cl1).filter(cl1.name==name_obj1).first()
    obj2 = world.session.query(cl2).filter(cl2.name==name_obj2).first()

    assert obj_has_attr(obj1, obj2, world.db_classes[class_name2])


@step(r'create <task> "(.*)" with project "(.*)", add task to session')
def check_create_task_with_args(step, task_name, project_name):
    task = task_script.create_task(world.session, task_name, project_name=project_name)
    world.session.add(task)


def obj_has_attr(obj1, obj2, tuple_obj2):
    """Summary

    Args: obj1:a sqlalchemy object
          tuple_obj2:named tuple with fields ("cl, collection, scalar")

    Returns: list or scalar of attribute
    """
    scalar = tuple_obj2.scalar
    collection = tuple_obj2.collection

    try:
        attribute = getattr(obj1, scalar)
        return attribute is obj2
    except:
        try:
            attribute = getattr(obj1, collection)
            return obj2 in attribute
        except:
            return False


@step(r'mark <task> named "(.*)" complete')
def test_mark_task_complete(step, task_name):
    assert task_script.mark_task_complete(world.session, task_name)

@step(r'call to "(.*)" returns a dict with <(\d)> keys')
def test_funcall_returns_dict_with_correct_num_keys(step, func_name, num):
    test_dict = tag_script.get_tags_as_dict(world.session)
    num = int(num)
    assert len(test_dict.keys()) == num

@step(r'call to "(.*)" returns a set with <(\d)> keys')
def test_get_tag_name_set_returns_set_with_correct_num_keys(step, func_name, num):
    test_set = tag_script.get_tag_name_set(world.session)
    num = int(num)
    assert len(test_set) == num

