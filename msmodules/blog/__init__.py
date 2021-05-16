from flask import Flask,Blueprint, jsonify, request
module_bp = Blueprint('blog_bp', __name__)
module_prefix = '/blog'

#from app.views.AuthEndpoints import Authenticate
#from app.views.AuthEndpoints import Renew

#module_bp.add_url_rule("/api/auth/authenticate", view_func=Authenticate.as_view("example_apisauth"))
#module_bp.add_url_rule("/api/auth/renew", view_func=Renew.as_view("example_apisauthrenew"))



