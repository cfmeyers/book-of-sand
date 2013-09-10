from init_db import *
import db_utils

def get_tags_as_dict(session):
    """Given a session object, create a dictionary of tags of the form
    {tag_name:tag} where tag_name is a string

    Args: session:sqlalchemy session object

    Returns: dictionary
    """
    tag_dict = {}
    tag_list = session.query(Tags)
    for tag in tag_list:
        tag_dict[tag.name] = tag

    return tag_dict

def get_tag_name_set(session):
    """Given a session object, create a set of tag names

    Args: session:sqlalchemy session object

    Returns: set
    """
    tag_set = set([])
    tag_list = session.query(Tags)
    for tag in tag_list:
        tag_set.add(tag.name)

    return tag_set



