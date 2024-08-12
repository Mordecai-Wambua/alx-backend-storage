#!/usr/bin/env python3
"""Function that inserts a new document in a collection based on kwargs."""


def insert_school(mongo_collection, **kwargs):
    """Return the new _id of inserted document."""
    doc = {}
    for k, v in kwargs.items():
        doc[k] = v

    result = mongo_collection.insert_one(doc)
    return result.inserted_id
