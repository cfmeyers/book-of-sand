Feature: Create a tag
    As a user
    I want to create tasks using SQLalchemy ORM
    So that I can add them to the database

    Scenario: Create a <tag> and objects to associate with the <tag>
        Given an empty database
        Then I create a <tag> named "SICP" and add it to the session

        #A tag can have an event
        And I create a <event> named "downloaded SICP" and add it to the session
        And I add the <tag> named "SICP" to the <event> named "downloaded SICP"
        #A tag can have an task
        And I create a <task> named "read ch1" and add it to the session
        And I add the <tag> named "SICP" to the <task> named "read ch1"

        #A tag can have an project
        And I create a <project> named "learn fp" and add it to the session
        And I add the <tag> named "SICP" to the <project> named "learn fp"

        And commit the session to the db


    Scenario: verify connections between <tag> and above objects
        Then the <tag> named "SICP" has a many-to-many relationship with the <event> named "downloaded SICP"
        Then the <tag> named "SICP" has a many-to-many relationship with the <task> named "read ch1"
        Then the <tag> named "SICP" has a many-to-many relationship with the <project> named "learn fp"
        Then the <tag> "SICP" has <event> "downloaded SICP"
        Then the <tag> "SICP" has <task> "read ch1"
        Then the <tag> "SICP" has <project> "learn fp"



