Feature: Create a tag
    As a user
    I want to create tasks using SQLalchemy ORM
    So that I can add them to the database


Scenario: Empty database
    Given an empty database
    When I create a tag named "workout" and add it to the session
    Then I have a non-empty database
