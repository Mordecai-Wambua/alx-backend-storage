#!/usr/bin/env python3
"""Function that lists all documents in a collection."""
import pprint


def list_all(mongo_collection):
    """Return the documents."""
    output = []
    for doc in mongo_collection.find():
        output.append(doc)
    return output
