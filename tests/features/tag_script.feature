Feature: manipulate tags with tag_script.py
    As a user
    I want to get tag objects from the database in various ways

    Scenario: add three new tags to an empty database
        Given an empty database
        When I create a <tag> named "alfred" and add it to the session
        And I create a <tag> named "dev" and add it to the session
        And I create a <tag> named "command line" and add it to the session
        And commit the session to the db

    Scenario: get a dictionary of all the tags in a database
        Given a database with <3> <tag> objects
        Then a call to "tag_script.get_tags_as_dict" returns a dict with <3> keys
        Then a call to "tag_script.get_tag_name_set" returns a set with <3> keys
