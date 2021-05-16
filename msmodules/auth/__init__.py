from flask import Flask,Blueprint, jsonify, request
module_bp = Blueprint('auth_bp', __name__)
module_prefix = '/auth'

from .views.AuthEndpoints import Authenticate
from .views.AuthEndpoints import Renew

module_bp.add_url_rule("/authenticate", view_func=Authenticate.as_view("example_apisauth"))
module_bp.add_url_rule("/renew", view_func=Renew.as_view("example_apisauthrenew"))



