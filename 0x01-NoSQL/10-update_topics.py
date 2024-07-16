#!/usr/bin/env python3
"""Module for task 10."""


def update_topics(mongo_collection, name, topics):
    """Changes all topics of a school's document based on the name."""
    mongo_collection.update_many(
        {'name': name},
        {'$set': {'topics': topics}}
    )
