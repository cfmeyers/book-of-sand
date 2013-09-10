Feature: Create an event
    As a user
    I want to create events using SQLalchemy ORM
    So that I can add them to the database

    Scenario: Create an <event> and objects to associate with the <event>
        Given an empty database
        Then I create a <event> named "changed baby's diapers" and add it to the session

        #An event can have a project
        And I create a <project> named "babysit" and add it to the session
        And I add the <event> named "changed baby's diapers" to the <project> named "babysit"

        #An event can have a tag
        And I create a <tag> named "baby" and add it to the session
        And I add the <event> named "changed baby's diapers" to the <tag> named "baby"

        And commit the session to the db

    Scenario: verify connections between <event> and above objects
        Then the <project> named "babysit" has a one-to-many relationship with the <event> named "changed baby's diapers"
        Then the <event> named "changed baby's diapers" has a many-to-many relationship with the <tag> named "baby"