#!/usr/bin/env python3
"""Module for task 11."""


def schools_by_topic(mongo_collection, topic):
    """Returns the list of schools having a specific topic."""
    filtered = {
        'topics': {
            '$elemMatch': {
                '$eq': topic,
            },
        },
    }
    return [item for item in mongo_collection.find(filtered)]
