from flask.views import MethodView
from flask import request, jsonify, send_file
import db
from models.user import User
from models.group import Group
import pprint
from app import auth
from app import SUCCESS_STR
from app import FAIL_STR
from app import STATUS_KEY
from app import ERROR_KEY

import sys, os

from sqlalchemy import and_, or_, not_

# /cdn/suneditor/upload
class Uploads(MethodView):

#    @auth.jwt_private    
    def get(self,filepath):
        print("SunEditorCompat::get()")
        print('/cdn/uploads called for: ' + str(filepath))
        return send_file(os.path.join('/upload',filepath))
