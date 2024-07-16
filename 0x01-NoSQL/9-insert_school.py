#!/usr/bin/env python3
"""Module for Task 9."""


def insert_school(mongo_collection, **kwargs):
    """Inserts a new document in a collection."""
    collection = mongo_collection.insert_one(kwargs)
    return collection.inserted_id
