# from lettuce import world
from lettuce import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *
from init_db import Base, Tags, Tasks, Events
from termcolor import cprint

@before.all
def say_hello():
    print "\n"*10
    # cprint("LETTUCE WILL START TO RUN TESTS RIGHT NOW...", 'green')


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
    world.db_classes = {"tag":Tags, "task":Tasks, "event":Events}
    world.obj_dict   = {}
    print ""
    cprint("====================================================", 'cyan')
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

            print ""
            cprint("-SCENARIO-FAILED: "+str(scenario.name), 'red')
            for step in steps:
                if step.failed:
                    cprint(" "+str(step.described_at.line)+"**"+ str(step.sentence), 'red')
                elif step.passed:
                    cprint(" "+str(step.described_at.line)+"  "+str(step.sentence), 'green')
                else:
                    cprint(" "+str(step.described_at.line)+"**" + str(step.sentence), 'yellow')
            print ""
            return
    cprint("-SCENARIO-PASSED: "+str(scenario.name), 'green')


@after.each_feature
def teardown_feature(feature):
    world.engine        = None
    world.session       = None
    world.db_classes    = None
    world.obj_dict      = None
    world.failed_steps  = None
    world.untried_steps = None
    # cprint("END FEATURE: "+feature.name, 'white', 'on_grey')

@after.all
def last_thing(total):
    for item in total.proposed_definitions:
        print "   "
        cprint("Needs a definition:", 'magenta')
        cprint(str(item.sentence), 'yellow')
