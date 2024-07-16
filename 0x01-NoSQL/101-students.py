#!/usr/bin/env python3
"""Module for task 14."""


def top_students(mongo_collection):
    """Prints all students in a collection sorted by average score."""
    student_list = mongo_collection.aggregate(
        [
            {
                '$project': {
                    '_id': 1,
                    'name': 1,
                    'averageScore': {
                        '$avg': {
                            '$avg': '$topics.score',
                        },
                    },
                    'topics': 1,
                },
            },
            {
                '$sort': {'averageScore': -1},
            },
        ]
    )
    return student_list