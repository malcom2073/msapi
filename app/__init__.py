from flask import Flask, jsonify, request
app = Flask(__name__)
app.config['SECRET_KEY'] = "asfdsafdsadfsafdsadffdsa"
#app.config['SQLALCHEMY_URL'] = "sqlite:///"


from app.views.UserEndpoint import UserEndpoint
from app.views.UsersEndpoint import UsersEndpoint
from app.views.GroupsEndpoint import GroupsEndpoint
from app.views.AuthEndpoints import Authenticate
from app.views.AuthEndpoints import Renew

app.add_url_rule("/users/<userid>", view_func=UserEndpoint.as_view("example_api"))
app.add_url_rule("/users", view_func=UsersEndpoint.as_view("example_apis"))
app.add_url_rule("/groups", view_func=GroupsEndpoint.as_view("example_apisgroup"))
app.add_url_rule("/auth/authenticate", view_func=Authenticate.as_view("example_apisauth"))
app.add_url_rule("/auth/renew", view_func=Renew.as_view("example_apisauthrenew"))



