__author__ = 'Aishwarya Pradhan'

from flask import Flask, request, abort
from redis_tasks import get_request, count_request
from functools import wraps

app = Flask(__name__)

# replace this with authentication key variable name
authkey = "auth-token"

# dummy key
secret_key = "arpar"


# Below 3 methods are required

def check_alloted_request(auth_token):
    # TODO write logic to getting alloted requests
    return 30


def check_auth_token(auth_token):
    # TODO write the logic to check auth_token
    if auth_token == secret_key:
        return True
    else:
        return False


# decorator copied shamelessly from stackoverflow. Thanks to TkTech
def validate_request(myrequest):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            ret = f(*args, **kwargs)
            # logic start
            request_auth_token = myrequest.headers.get(authkey)
            if check_auth_token(request_auth_token):
                if count_request(request_auth_token) < check_alloted_request(request_auth_token):
                    get_request(request_auth_token)
                else:
                    abort(403)
                    # return "Why don't you f*** off"
            else:
                abort(401)
            # logic end

            return ret

        return wrapped

    return decorator


# Now, you can use @validate_request(request) decorator wherever you want the check enabled


@app.route('/')
@validate_request(request)
def hello_world():
    return "You are love"


if __name__ == '__main__':
    app.run()
