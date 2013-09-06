Feature: Create an event
    As a user
    I want to create *events* using SQLalchemy ORM
    So that I can add them to the database

Scenario: Empty database
    Given an empty database
    When I create an event object with a name of BABY WET HER DIAPER and date of today
    And add the event to the session
    And I create a tag object with a name of BABY
    And add the tag to the session
    And I add the tag to the event
    And commit the session
    And query the database for the event object
    Then the event object will have a list consisting of the single tag I had added
