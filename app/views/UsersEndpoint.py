from flask import request
from flask.views import MethodView
import db
from models.user import User
from models.group import Group
from models.usermetadata import UserMetadata
import pprint
from app import auth
from app import SUCCESS_STR
from app import FAIL_STR
from app import STATUS_KEY
from app import ERROR_KEY
class UsersEndpoint(MethodView):

    @auth.jwt_private    
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
        return {STATUS_KEY:SUCCESS_STR,'users':retval},200

    @auth.jwt_private    
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
                        metadata: [
                            { key1: value1  },
                            { key2: value2 }
                        ]
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
            return {STATUS_KEY:FAIL_STR,ERROR_KEY:'Invalid group name entered'}
        user = User(name=userjson['name'],username=userjson['username'],password=userjson['password'],email=userjson['email'],groups=[group])
        metalist = []
        if 'metadata' in userjson:
            # Metadata exists, so insert it into the metadata table
            for item in userjson['metadata']:
                if len(item.keys()) > 1:
                    # Bad!
                    return {STATUS_KEY:FAIL_STR,ERROR_KEY:'Invalid metadata format'}
                key = list(item.keys())[0]
                value = item[list(item.keys())[0]]
                usermeta = UserMetadata(key=key,value=value)
                user.usermeta.append(usermeta)
                metalist.append(usermeta)
                print(item,flush=True)
        else:
            print("No metadata in userjson",flush=True)
        try:
            dbsession.add(user)
            for usermeta in metalist:
                dbsession.add(usermeta)
            dbsession.commit()
        except Exception as ex:
            print("unable to add user to DB")
            return {STATUS_KEY:FAIL_STR,ERROR_KEY:"Unable to add user: " + str(ex)}

        return {STATUS_KEY:SUCCESS_STR,'users':[user.as_obj()]},200

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

