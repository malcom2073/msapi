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
module_bp = Blueprint('cdn_bp', __name__)
module_prefix = '/cdn'
#import db
#import models
#from app.models.user import User
#from app.models.group import Group
#from app.models import userprofilefield as UserProfileField
#from modules.blog.python.models.msblogpost import MSBlogPost
import app
import os
from sqlalchemy import and_, or_, not_
from .views.suneditorcompat import SunEditorCompat
from .views.uploads import Uploads
#from .views.postcollection import PostCollection
#from .views.postresource import PostResource
#from .models.msblogpost import MSBlogPost
#module_bp.add_url_rule("/posts", view_func=PostCollection.as_view("example_apisauth"))
#module_bp.add_url_rule("/posts", view_func=PostCollection.as_view("example_apisauth"))
module_bp.add_url_rule("/suneditor/upload", view_func=SunEditorCompat.as_view("example_apisauth3"))
module_bp.add_url_rule("/uploads/<filepath>", view_func=Uploads.as_view("example_apisauth4"))

# Should there be a standard set of module endpoints?
# Something like: /getVersion, /getInfo, /getAuthor?
