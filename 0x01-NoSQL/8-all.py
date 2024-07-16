#!/usr/bin/env python3
"""Module for task 8."""


def list_all(mongo_collection):
    """Lists all documents in a collection."""
    return [item for item in mongo_collection.find()]
