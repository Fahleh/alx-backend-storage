#!/usr/bin/env python3
"""Module for task 12."""

from pymongo import MongoClient


def print_nginx_request_logs(nginx_collection):
    """Prints some stats about Nginx request logs."""
    print('{} logs'.format(nginx_collection.count_documents({})))
    print('Methods:')
    method_list = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in method_list:
        count = len(list(nginx_collection.find({'method': method})))
        print('\tmethod {}: {}'.format(method, count))
    stat_counter = len(list(
        nginx_collection.find({'method': 'GET', 'path': '/status'})
    ))
    print('{} status check'.format(stat_counter))


def run():
    """Provides some stats about Nginx logs stored in MongoDB."""
    mongo_client = MongoClient('mongodb://127.0.0.1:27017')
    print_nginx_request_logs(mongo_client.logs.nginx)


if __name__ == '__main__':
    run()
