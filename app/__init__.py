from flask import Flask, jsonify, request
app = Flask(__name__)
app.config['SECRET_KEY'] = "asfdsafdsadfsafdsadffdsa"
#app.config['SQLALCHEMY_URL'] = "sqlite:///"


from app.views.SingleUserMethod import SingleUserMethod
from app.views.UsersMethod import UsersMethod
from app.views.GroupsMethod import GroupsMethod

app.add_url_rule("/users/<userid>", view_func=SingleUserMethod.as_view("example_api"))
app.add_url_rule("/users", view_func=UsersMethod.as_view("example_apis"))
app.add_url_rule("/groups", view_func=GroupsMethod.as_view("example_apisgroup"))

