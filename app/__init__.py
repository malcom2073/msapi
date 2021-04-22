from flask import Flask, jsonify, request
app = Flask(__name__)
app.config['SECRET_KEY'] = "asfdsafdsadfsafdsadffdsa"
#app.config['SQLALCHEMY_URL'] = "sqlite:///"


from app.views.UserEndpoint import UserEndpoint
from app.views.UsersEndpoint import UsersEndpoint
from app.views.GroupsEndpoint import GroupsEndpoint

app.add_url_rule("/users/<userid>", view_func=UserEndpoint.as_view("example_api"))
app.add_url_rule("/users", view_func=UsersEndpoint.as_view("example_apis"))
app.add_url_rule("/groups", view_func=GroupsEndpoint.as_view("example_apisgroup"))

