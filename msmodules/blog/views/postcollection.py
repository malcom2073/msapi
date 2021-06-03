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

import sys
from ..models.msblogpost import MSBlogPost
from sqlalchemy import and_, or_, not_

# /posts
class PostCollection(MethodView):

#    @auth.jwt_private
    def get(self):
        """
        Endpoint to get a specific user
        This is using docstrings for specifications.
        ---
        parameters:
            - in: path
              name: userid
              schema:
                  type: integer
              required: true
        responses:
            200:
                description: A user object
            401:
                description: Permission denied
        """

        jwt = auth.getJwt(request)
        print("JWT!!!")
        pprint.pprint(jwt)
        print("JWT!!!")
        print(jwt)
        uid = None
        if jwt:
            uid = jwt['user_id']
        print("User ID: " + str(uid))
    #    jwt = getJwt(request)
    #    post_data = request.get_json()
    #    pprint.pprint(post_data)
        #print('Index: ' + str(post_data.get('id')))
    #    print('Last: ' + str(post_data.get('last')))
        sys.stdout.flush()
        try:
            dbsession = db.AppSession()
            #filter(or_(User.name == 'ed', User.name == 'wendy'))
            #postlist = dbsession.query(MSBlogPost).filter((MSBlogPost.published == True) | (MSBlogPost.published == False & MSblogPost.user = )).order_by(MSBlogPost.timestamp.desc()).all()
            postlist = None
            if uid is not None:
                postlist = dbsession.query(MSBlogPost).filter(or_(MSBlogPost.published == True,MSBlogPost.user_id == uid)).order_by(MSBlogPost.timestamp.desc()).all()
            else:
                postlist = dbsession.query(MSBlogPost).filter(MSBlogPost.published == True).order_by(MSBlogPost.timestamp.desc()).all()
            #if jwt is not None:
            #    postlist = dbsession.query(MSBlogPost).filter(or_(MSBlogPost.published == True,MSBlogPost.user_id == jwt['user_id'])).order_by(MSBlogPost.timestamp.desc()).all()
            #else:
            #    postlist = dbsession.query(MSBlogPost).order_by(MSBlogPost.timestamp.desc()).all()
            jsonresponse = jsonify({STATUS_KEY:SUCCESS_STR,'posts': postlist})
            dbsession.close()
            print("Postcount: " + str(len(postlist)))
            sys.stdout.flush()

            if postlist is None or len(postlist) == 0:
                print("No posts")
                return {STATUS_KEY:SUCCESS_STR,'posts':[]},200
                return jsonify({STATUS_KEY:FAIL_STR,ERROR_KEY:'No Posts'})
            return jsonresponse
        except Exception as e:
            return jsonify({STATUS_KEY:FAIL_STR,ERROR_KEY:str(e)})
        return jsonify({STATUS_KEY:SUCCESS_STR})

        #        users = manager.getAllUsers()
        dbsession = db.AppSession()
        user = dbsession.query(User).filter(User.id == userid).first()
        pprint.pprint(user)
        if user is None:
            return {STATUS_KEY:FAIL_STR,ERROR_KEY:"No valid User for userid " + str(userid) + " found"},200
        return {STATUS_KEY:SUCCESS_STR,'users':[user.as_obj()]},200
#        user = manager.getUser(int(userid))
#        return {'id' : user.id, 'username':user.username,'name': user.name,'groupname':user.groupname,'password':user.password,'state':user.state},200

    @auth.jwt_private    
    def post(self):
        jwt = auth.getJwt(request)
        print("JWT!!!")
        pprint.pprint(jwt)
        print("JWT!!!")
        print(jwt)
        uid = None
        if jwt:
            uid = jwt['user_id']
        print("User ID: " + str(uid))
        sys.stdout.flush()

#        return {STATUS_KEY:FAIL_STR,ERROR_KEY:"Not implemented: User: " + str(uid)},200

        userjson = request.get_json()
        user = MSBlogPost()
        try:
            user.user_id = uid
            user.content = userjson['content']
            user.title = userjson['title']
            user.timestamp = userjson['timestamp']
            user.published = False
            dbsession = db.AppSession()
            dbsession.add(user)
            dbsession.commit()
        except Exception as ex:
            return {STATUS_KEY:FAIL_STR,'post':userjson,'exception': str(ex)},200
        return {STATUS_KEY:SUCCESS_STR,'post':user.as_obj()}
#        user = manager.addUser(userjson['username'],userjson['name'],userjson['groupname'],userjson['password'],userjson['state'])
#        return {'result':SUCCESS_STR,'result':{'id' : user.id, 'username':user.username,'name': user.name,'groupname':user.groupname,'password':user.password,'state':user.state}},200

    @auth.jwt_private    
    def put(self):
        """ Responds to PUT requests """
        return "Responding to a PUT request"

    @auth.jwt_private    
    def patch(self,userid):
        """ Responds to PATCH requests """
        dbsession = db.AppSession()
        user = dbsession.query(User).filter(User.id == userid).first()
        pprint.pprint(user)
        if user is None:
            return {STATUS_KEY:FAIL_STR,ERROR_KEY:"No valid User for userid " + str(userid) + " found"},200
        userjson = request.get_json()
        # This will contain the changes to make tothis use as list of  KVP
        # [{"key":"value"}]
        print(userjson)
        for patch in userjson:
            #pprint.pprint(patch)
            print(patch)
            setattr(user,patch,userjson[patch])
#            user[patch] = userjson[patch]
        try:
            dbsession.commit()
            return {STATUS_KEY:SUCCESS_STR,'users':[user.as_obj()]},200
        except:
            dbsession.rollback()
            return {STATUS_KEY:FAIL_STR,ERROR_KEY:"Unable to commit!"},200

        return "Responding to a PATCH request"

    @auth.jwt_private    
    def delete(self):
        """ Responds to DELETE requests """
        return "Responding to a DELETE request"


