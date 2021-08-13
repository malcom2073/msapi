#module_bp.add_url_rule("/api/auth/authenticate", view_func=Authenticate.as_view("example_apisauth"))
#module_bp.add_url_rule("/api/auth/renew", view_func=Renew.as_view("example_apisauthrenew"))



from flask import Blueprint, render_template, Flask, jsonify, request,send_file
import pprint
import hashlib
import random
import string
import datetime
import jwt
import sys # For sys.stdout.flush()
#from PIL import Image
#from util import getJwt, getAuthToken
from app.auth import jwt_private
module_bp = Blueprint('mc_bp', __name__)
module_prefix = '/mc'
#import db
#import models
#from app.models.user import User
#from app.models.group import Group
#from app.models import userprofilefield as UserProfileField
#from modules.blog.python.models.msblogpost import MSBlogPost
import app
import os
from sqlalchemy import and_, or_, not_
from .views.serverstat import ServerStats
from .views.ServerChat import ServerChat
from .views.serverstat2 import ServerStats2
#from .views.postcollection import PostCollection
#from .views.postresource import PostResource
#from .models.msblogpost import MSBlogPost
#module_bp.add_url_rule("/posts", view_func=PostCollection.as_view("example_apisauth"))
#module_bp.add_url_rule("/posts", view_func=PostCollection.as_view("example_apisauth"))
module_bp.add_url_rule("/serverstats", view_func=ServerStats.as_view("example_apisauth5"))
module_bp.add_url_rule("/serverstats2", view_func=ServerStats2.as_view("example_apisauth52"))
module_bp.add_url_rule("/serverchat", view_func=ServerChat.as_view("example_apisauth53"))

# Should there be a standard set of module endpoints?
# Something like: /getVersion, /getInfo, /getAuthor?
