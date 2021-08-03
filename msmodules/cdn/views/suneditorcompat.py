from flask.views import MethodView
from flask import request, jsonify
import db
from models.user import User
from models.group import Group
import pprint
from app import auth
from app import SUCCESS_STR
from app import FAIL_STR
from app import STATUS_KEY
from app import ERROR_KEY
from PIL import Image
import os

import sys
from sqlalchemy import and_, or_, not_

# /cdn/suneditor/upload
class SunEditorCompat(MethodView):

    @auth.jwt_private    
    def post(self):
        print("SunEditorCompat::post()")
        if request.files:
            print("Has files")
        jwt = auth.getJwt(request)
        print("/upload called")
        sys.stdout.flush()
        pprint.pprint(request.files)
        pprint.pprint(request)
        formdict = request.form.to_dict()
        pprint.pprint(formdict)
        for f in request.files:
            print("File: " + f)
            pprint.pprint(request.files.get(f))
            filestor = request.files.get(f)
            filestor.save(os.path.join('/upload',f))
            im = Image.open(os.path.join('/upload',f))
            size = im.width,im.height
            if 'inputHeight' in formdict and 'inputWidth' in formdict:
                size = int(formdict['inputWidth']) if formdict['inputWidth'] != '' else im.width, int(formdict['inputHeight']) if formdict['inputHeight'] != '' else im.height
            im.thumbnail(size)
            if im.mode in ("RGBA", "P"):
                im = im.convert("RGB") 
            im.save(os.path.join('/upload',"thumbnail." + f), "JPEG")
        #pprint.pprint(formdict['file'])
        #pprint.pprint(formdict['image[image]'])
        sys.stdout.flush()
        post_data = request.get_json()
        pprint.pprint(post_data)
        return jsonify({
            'status':'success',
            'path':"/api/cdn/uploads/" + f,
            'thumbnail':"/api/cdn/uploads/thumbnail." + f
            })
#        print("JWT!!!")
#        pprint.pprint(jwt)
#        print("JWT!!!")
#        print(jwt)
#        uid = None
#        if jwt:
#            uid = jwt['user_id']
#        print("User ID: " + str(uid))
        sys.stdout.flush()

#        return {STATUS_KEY:FAIL_STR,ERROR_KEY:"Not implemented: User: " + str(uid)},200

#        userjson = request.get_json()
        #user = MSBlogPost()
        #try:
        #    user.user_id = uid
        #    user.content = userjson['content']
        #    user.title = userjson['title']
        #    user.timestamp = userjson['timestamp']
        #    user.published = False
        #    dbsession = db.AppSession()
        #    dbsession.add(user)
        #    dbsession.commit()
        #except Exception as ex:
        #    return {STATUS_KEY:FAIL_STR,'post':userjson,'exception': str(ex)},200
        return {STATUS_KEY:FAIL_STR,ERROR_KEY:"Unimplemented"}
#        user = manager.addUser(userjson['username'],userjson['name'],userjson['groupname'],userjson['password'],userjson['state'])
#        return {'result':SUCCESS_STR,'result':{'id' : user.id, 'username':user.username,'name': user.name,'groupname':user.groupname,'password':user.password,'state':user.state}},200
