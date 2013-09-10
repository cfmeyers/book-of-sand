from lettuce import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *
from init_db import Base, Tags, Tasks, Events, Projects
from termcolor import cprint
from collections import namedtuple

@before.all
def say_hello():
    world.focus = False #global variable that, when True, stops all printing to terminal

@before.each_feature
def feature_setup(feature):
    world.failed_steps  = []
    world.untried_steps = []
    world.passed_steps  = []
    world.scenarios     = {}
    world.engine        = create_engine('sqlite:///:memory:')
    Session             = sessionmaker(bind=world.engine)
    world.session       = Session()
    Base.metadata.create_all(world.engine)
    tbl = namedtuple("tbl", "cl, collection, scalar")
    world.db_classes = {"tag":     tbl(Tags,   "tags", "tag"),
                        "task":    tbl(Tasks,  "tasks", "task"),
                        "event":   tbl(Events, "events", "event"),
                        "project": tbl(Projects,"projects", "project")}
                        # "person":  tbl(Persons,"persons"),
                        # "place":   tbl(Places, "places")}
    world.obj_dict   = {}
    if not world.focus:
        cprint(u'\u250f'+""+u'\u2501'*70, 'cyan')
        cprint(u'\u2503'+"  ", 'cyan', attrs=['bold'], end="")
        cprint("FEATURE: "+feature.name, 'cyan', attrs=['underline', 'bold'])

@before.each_scenario
def scenario_setup(scenario):
    world.scenarios[scenario.name] = []


@after.each_step
def teardown_some_step(step):
    world.scenarios[step.scenario.name].append(step)
    if step.failed:
        world.failed_steps.append(step)
    elif step.passed:
        world.passed_steps.append(step)
    else:
        world.untried_steps.append(step)

@after.each_scenario
def scenario_rundown(scenario):
    steps = world.scenarios[scenario.name]
    for step in steps:
        if step in world.untried_steps or step in world.failed_steps:

            cprint(u'\u2503'+"  ", 'cyan', attrs=['bold'])
            print ""
            cprint(u'\u2503'+"  ", 'cyan', attrs=['bold'], end="")
            cprint(" -SCENARIO-FAILED: "+str(scenario.name), 'red')
            step_stepper(steps)
            # for step in steps:
            #     if step.failed:
            #         cprint(" "+str(step.described_at.line)+"**"+ str(step.sentence), 'red')
            #         world.focus = True
            #     elif step.passed:
            #         cprint(" "+str(step.described_at.line)+"  "+str(step.sentence), 'green')
            #     else:
            #         cprint(" "+str(step.described_at.line)+"**" + str(step.sentence), 'yellow')
            #         world.focus = True
            # print ""
            return
        else:
            # step_stepper(steps)
            pass
    if not world.focus:
        cprint(u'\u2503'+"  ", 'cyan', attrs=['bold'], end="")
        cprint(" -SCENARIO-PASSED: "+str(scenario.name), 'green')


@after.each_feature
def teardown_feature(feature):
    world.engine        = None
    world.session       = None
    world.db_classes    = None
    world.obj_dict      = None
    world.failed_steps  = None
    world.untried_steps = None
    # if not world.focus:
        # cprint(u'\u2517'+""+u'\u2501'*70, 'cyan')

@after.all
def last_thing(total):
    cprint(u'\u2588'*85, 'white')

def step_stepper(steps):
    for step in steps:
        if step.failed:
            cprint(" "+str(step.described_at.line)+"**"+ str(step.sentence), 'red')
            world.focus = True
        elif step.passed:
            cprint(" "+str(step.described_at.line)+"  "+str(step.sentence), 'green')
        else:
            cprint(" "+str(step.described_at.line)+"**" + str(step.sentence), 'yellow')
            world.focus = True
    print ""


