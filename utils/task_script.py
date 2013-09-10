from init_db import *
from db_utils import get_or_create
from datetime import datetime


def create_task(session, task_name, tag_names=[], project_name=None):
     """

    Args: session:sqlalchemy session object
           task_name:string
           tag_names:list of strings
           project_name:string

     Returns: task object
     """
     task = Tasks(task_name)
     if tag_names:
        for tag_name in tag_names:
            tag = get_or_create(session, Tags, tag_name)
            assert tag != None
            task.tags.append(tag)

     if project_name:
        project = get_or_create(session, Projects, project_name)
        task.project = project

     return task

def mark_task_complete(session, task_name):
    """Finds the task in db, marks it complete

    Args: session:sqlalchemy session object
           task_name:string

    Returns: returns True if task found and marked complete, False otherwise
    """
    task = session.query(Tasks).filter(Tasks.name==task_name).first()
    if not task:
        return False
    if not task.date_completed:
        task.date_completed = datetime.now()
        return True
    return False







