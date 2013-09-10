Feature: manipulate tasks with task_script.py
    As a user
    I want to add a task to the database by making a calls to task_script.py from a different file

    Scenario: add a task with only a name to the database
        Given an empty database
        Then I call create_task with the name "buy milk", get back a task object, add to session

    Scenario: add a task with a name and two tags to the database
        When I create a <tag> named "flowers" and add it to the session
        And create a <tag> named "girlfriend" and add it to the session
        And create <task> "buy roses" with tags "flowers", "girlfriend", add task to session
        Then the <task> "buy roses" has <tag> "flowers"
        Then the <task> "buy roses" has <tag> "girlfriend"

    Scenario: add a task with a name and two tags to the db, but the two tags have not been created yet
        And create <task> "make coffee" with tags "caffeine", "breakfast", add task to session
        Then the <task> "make coffee" has <tag> "caffeine"
        Then the <task> "make coffee" has <tag> "breakfast"

    Scenario: add a task with a name and a project
        When I create a <project> named "feed parser" and add it to the session
        And create <task> "build db" with project "feed parser", add task to session
        Then the <task> "build db" has <project> "feed parser"

    Scenario: complete a task by calling complete_task
        When I create a <task> named "buy taco" and add it to the session
        Then mark <task> named "buy taco" complete


