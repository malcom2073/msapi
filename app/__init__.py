# REST string types.
# These are used to indicate success/failure of messages, and what the state string is in the message for checking that.
# These should never change, but I've changed them twice, so they're "variables" now
SUCCESS_STR = 'success'
FAIL_STR = 'failure'
STATUS_KEY = 'status'
ERROR_KEY = 'error'

from flask import Flask, jsonify, request
app = Flask(__name__)
app.config['SECRET_KEY'] = "asfdsafdsadfsafdsadffdsa"
#app.config['SQLALCHEMY_URL'] = "sqlite:///"


from app.views.UserEndpoint import UserEndpoint
from app.views.UsersEndpoint import UsersEndpoint
from app.views.GroupsEndpoint import GroupsEndpoint

app.add_url_rule("/api/users/<userid>", view_func=UserEndpoint.as_view("example_api"))
app.add_url_rule("/api/users", view_func=UsersEndpoint.as_view("example_apis"))
app.add_url_rule("/api/groups", view_func=GroupsEndpoint.as_view("example_apisgroup"))
#app.add_url_rule("/api/db/create", view_func=Renew.as_view("example_apisauthrenew"))
#app.add_url_rule("/api/db/query", view_func=Renew.as_view("example_apisauthrenew"))




def loadModules():
    print("loading")
    import os
    import importlib
    d = 'msmodules/'
    for o in os.listdir(d):
        if os.path.isdir(os.path.join(d,o)):
            i = importlib.import_module(".",'msmodules.' + o + '')
            app.register_blueprint(i.module_bp,url_prefix="/api" + i.module_prefix)
            print("Imported module")
            print(i)
            print("Dir: " + os.path.join(d,o))

loadModules()
