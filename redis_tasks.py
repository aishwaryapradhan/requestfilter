__author__ = 'Aishwarya Pradhan'

import redis

# Setup your redis server
r_server = redis.Redis("localhost")

# TODO add your logics as per your business needs to clean or reset the amount of hits
def get_request(secret_key):
    r_server.incr(secret_key)


def count_request(secret_key):
    count = r_server.get(secret_key)
    if count:
        return int(count)
    else:
        return 0
