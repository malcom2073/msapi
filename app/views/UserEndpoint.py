from flask.views import MethodView
import db
from models.user import User
from models.group import Group
import pprint
# /users/<userid>
class UserEndpoint(MethodView):
    
    def get(self,userid):
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
        #        users = manager.getAllUsers()
        dbsession = db.AppSession()
        user = dbsession.query(User).filter(User.id == userid).first()
        pprint.pprint(user)
        if user is None:
            return {'status':'failure','error':"No valid User for userid " + str(userid) + " found"},200
        return {'status':'success','result':user.as_obj()},200
#        user = manager.getUser(int(userid))
#        return {'id' : user.id, 'username':user.username,'name': user.name,'groupname':user.groupname,'password':user.password,'state':user.state},200

    def post(self,userid):
       
        userjson = request.get_json()
        user = manager.addUser(userjson['username'],userjson['name'],userjson['groupname'],userjson['password'],userjson['state'])
        return {'result':'success','result':{'id' : user.id, 'username':user.username,'name': user.name,'groupname':user.groupname,'password':user.password,'state':user.state}},200

    def put(self):
        """ Responds to PUT requests """
        return "Responding to a PUT request"

    def patch(self):
        """ Responds to PATCH requests """
        return "Responding to a PATCH request"

    def delete(self):
        """ Responds to DELETE requests """
        return "Responding to a DELETE request"


