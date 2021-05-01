from flask import request
from flask.views import MethodView
import db
from models.group import Group
import pprint

from app import auth


class GroupsEndpoint(MethodView):
    
    @auth.jwt_private    
    def get(self):
        """
        Endpoint to get a list of groups
        This is using docstrings for specifications.
        ---
        responses:
            200:
                description: A user object
            401:
                description: Permission denied
        """
#        users = manager.getAllUsers()
        dbsession = db.AppSession()
        users = dbsession.query(Group).all()
        pprint.pprint(users)
        retval = []
        for user in users:
            retval.append(user.as_obj())
        return {'status':'success','groups':retval},200

    @auth.jwt_private    
    def post(self):
        """
        Endpoint to create a new group
        This endpoint allows authenticated and authorized users to create new groups
        ---
        summary: This isa summary
        requestBody:
            description: Optional description in *Markdown*
            required: true
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/User'
                    example:
                        name: bob
                        username: bobinabout
                        email: bob@asdf.com
                        password: bobingabout123
                        groupname: admin
                        state: new
        responses:
            200:
                description: A user object
            401:
                description: Permission denied
        """
        # This should be { "name":"groupname" }
        groupjson = request.get_json()
        dbsession = db.AppSession()
        group = Group(name=groupjson['name'])
        try:
            dbsession.add(group)
            dbsession.commit()
        except Exception as ex:
            print("unable to add group to DB")
            return {'status':'failure','error':"Unable to add group: " + str(ex)}
        return {'status':'success','groups':[group.as_obj()]},200
