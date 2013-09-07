Feature: Get information about a sqlalchemy table
    As the developer
    I want to have correct information about my sqlalchemy tables

Scenario: An empty table has 0 rows
    Given an empty database
    Then the tag table has no rows
    Then I create a tag named "workout" and add it to the session
    Then I create a tag named "baby" and add it to the session
    Then the tag table has some rows
    Then the tag table has 2 rows
    Then I create a tag named "workstation setup" and add it to the session
    Then the tag table has 3 rows



