Feature: Create a task
    As a user
    I want to create tasks using SQLalchemy ORM
    So that I can add them to the database

Scenario: Empty database
    Given an empty database
    When I create a task named "do 3 pushups" and add it to the session
    And I create a tag named "workout" and add it to the session
    And commit the session to the db
    Then the task named "do 3 pushups" is autoassigned an id of 1
    Then the tag named "workout" is autoassigned an id of 1

Scenario: Database has a tag and a task
    Given a database with a task named "do 3 pushups"
    And a database with a tag named "workout"
    When I add the tag named "workout" to the task named "do 3 pushups"
    Then the tag named "workout" has a list == [task named "do 3 pushups"]



