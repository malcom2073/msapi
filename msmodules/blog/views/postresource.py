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
class PostResource(MethodView):

    def get(self,postid):
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
        uid = None
        if jwt:
            uid = jwt['user_id']
        try:
            dbsession = db.AppSession()
            #filter(or_(User.name == 'ed', User.name == 'wendy'))
            #postlist = dbsession.query(MSBlogPost).filter((MSBlogPost.published == True) | (MSBlogPost.published == False & MSblogPost.user = )).order_by(MSBlogPost.timestamp.desc()).all()
            postlist = None
            if uid is not None:
                postlist = dbsession.query(MSBlogPost).filter(and_(or_(MSBlogPost.published == True,MSBlogPost.user_id == uid),MSBlogPost.id == postid)).order_by(MSBlogPost.timestamp.desc()).one()
            else:
                postlist = dbsession.query(MSBlogPost).filter(and_(MSBlogPost.published == True),MSBlogPost.id == postid).order_by(MSBlogPost.timestamp.desc()).one()
            if postlist is None:
                print("No posts")
                dbsession.close()
                return jsonify({STATUS_KEY:FAIL_STR,ERROR_KEY:'No Posts'})
            jsonresponse = jsonify({STATUS_KEY:SUCCESS_STR,'post': postlist})
            dbsession.close()
            sys.stdout.flush()

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
        return {STATUS_KEY:SUCCESS_STR,'user':user.as_obj()},200
#        user = manager.getUser(int(userid))
#        return {'id' : user.id, 'username':user.username,'name': user.name,'groupname':user.groupname,'password':user.password,'state':user.state},200

    @auth.jwt_private    
    def put(self,postid):
        """ Responds to PUT requests """
        return "Responding to a PUT request"

    @auth.jwt_private    
    def patch(self,postid):
        """ Responds to PATCH requests """
        dbsession = db.AppSession()
        post = dbsession.query(MSBlogPost).filter(MSBlogPost.id == postid).first()
        pprint.pprint(post)
        if post is None:
            return {STATUS_KEY:FAIL_STR,ERROR_KEY:"No valid Post for postid " + str(postid) + " found"},200
        postpatch = request.get_json()
        # This will contain the changes to make tothis use as list of  KVP
        # [{"key":"value"}]
        print(postpatch)
        for patch in postpatch:
            #pprint.pprint(patch)
            print(patch)
            setattr(post,patch,postpatch[patch])
#            user[patch] = userjson[patch]
        try:
            dbsession.commit()
            return {STATUS_KEY:SUCCESS_STR,'post':[post.as_obj()]},200
        except:
            dbsession.rollback()
            return {STATUS_KEY:FAIL_STR,ERROR_KEY:"Unable to commit!"},200

        return "Responding to a PATCH request"

    @auth.jwt_private    
    def delete(self):
        """ Responds to DELETE requests """
        return "Responding to a DELETE request"


