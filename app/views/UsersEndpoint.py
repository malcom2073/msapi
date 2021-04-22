from flask import request
from flask.views import MethodView
import db
from models.user import User
from models.group import Group
import pprint

class UsersEndpoint(MethodView):
    
    def get(self):
        """
        Endpoint to get a specific user
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
        users = dbsession.query(User).all()
        pprint.pprint(users)
        retval = []
        for user in users:
            retval.append(user.as_obj())
        return {'status':'success','users':retval},200

    def post(self):
        """
        Endpoint to create a new user
        This endpoint allows authenticated and authorized users to create new users
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
        userjson = request.get_json()
        dbsession = db.AppSession()
        group = dbsession.query(Group).filter(Group.name == userjson['groupname']).first()
        if group is None:
            # Invalid group! 
            return {'status':'failure','error':'Invalid group name entered'}
        user = User(name=userjson['name'],username=userjson['username'],password=userjson['password'],email=userjson['email'],groups=[group])
        try:
            dbsession.add(user)
            dbsession.commit()
        except Exception as ex:
            print("unable to add user to DB")
            return {'status':'failure','error':"Unable to add user: " + str(ex)}

        return {'status':'success','users':[user.as_obj()]},200

#    def put(self):
#        """ Responds to PUT requests """
#        return "Responding to a PUT request"
#
#    def patch(self):
#        """ Responds to PATCH requests """
#        return "Responding to a PATCH request"
#
#    def delete(self):
#        """ Responds to DELETE requests """
#        return "Responding to a DELETE request"

