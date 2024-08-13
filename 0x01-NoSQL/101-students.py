#!/usr/bin/env python3
"""Function that returns all students sorted by average score."""


def top_students(mongo_collection):
    """Return sorted student list."""
    for doc in mongo_collection.find():
        average = 0.0
        x = 0.0
        for scores in doc.get('topics'):
            x += scores['score']
        average = x / 3
        update = {'$set': {'averageScore': average}}
        mongo_collection.update_one({'_id': doc['_id']}, update)

    return mongo_collection.find().sort('averageScore', -1)
