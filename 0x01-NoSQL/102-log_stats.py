#!/usr/bin/env python3
"""Script that provides some stats about Nginx logs stored in MongoDB."""
from pymongo import MongoClient
from collections import Counter


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs.nginx
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    logs = db.count_documents({})
    print('{} logs\nMethods:'.format(logs))
    for method in methods:
        count = db.count_documents({'method': method})
        print('\tmethod {}: {}'.format(method, count))
    filter = {'method': 'GET', 'path': '/status'}
    print('{} status check'.format(db.count_documents(filter)))

    print("IPs:")
    store = []
    for doc in db.find():
        store.append(doc.get('ip'))
    counts = Counter(store)
    result = dict(counts.most_common(10))
    for k, v in result.items():
        print('\t{}: {}'.format(k, v))
