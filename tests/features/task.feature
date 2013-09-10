Feature: Create a task
    As a user
    I want to create tasks using SQLalchemy ORM
    So that I can add them to the database

    Scenario: Create a <task> and objects to associate with the <task>
        Given an empty database
        And I create a <task> named "drop off drycleaning" and add it to the session

        #A task can have a project
        And I create a <project> named "looking good" and add it to the session
        And I add the <task> named "drop off drycleaning" to the <project> named "looking good"

        #A task can have a tag
        And I create a <tag> named "chores" and add it to the session
        And I add the <task> named "drop off drycleaning" to the <tag> named "chores"

        And commit the session to the db

    Scenario: verify connections between <task> and above objects
        Then the <project> named "looking good" has a one-to-many relationship with the <task> named "drop off drycleaning"
        Then the <task> named "drop off drycleaning" has a many-to-many relationship with the <tag> named "chores"
