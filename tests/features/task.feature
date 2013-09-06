Feature: Create a task
    As a user
    I want to create tasks using SQLalchemy ORM
    So that I can add them to the database

Scenario: Empty database
    Given an empty database
    When I create a task object with a name of "DO 3 PUSHUPS"
    And add the task object with a name of "DO 3 PUSHUPS" to the session
    And I create a tag object with a name of "WORKOUT"
    And add the tag object with a name of "WORKOUT" to the session
    And commit the session
    And query the database for the task object with a name of "DO 3 PUSHUPS"
    Then the task object with a name of "DO 3 PUSHUPS" is autoassigned an id of 1
    And query the database for the tag object
    Then the tag object with a name of "WORKOUT" is autoassigned an id of 1

Scenario: Database has a tag object and a task object
    Given a database with a task with name of "DO 3 PUSHUPS"
    And a database with tag with name of "WORKOUT"
    When I add the tag to the task
    When I add the tag with name of "WORKOUT" to the task with name of "DO 3 PUSHUPS"
    Then the task object will have a list consisting of the single tag I had added
    Then the tag object will have a list consisting of the single task I had added



