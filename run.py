from flask import Flask, jsonify, request
from flask.views import MethodView
import json
app = Flask(__name__)
app.config['SECRET_KEY'] = 'asfdsafdsadfsafdsadffdsa'
app.config['SWAGGER'] = {}
app.config['SWAGGER']['openapi'] = '3.0.2'
from flasgger import Swagger
swagger = Swagger(app)
print("Running")

from dataclasses import dataclass
from dataclasses_serialization.json import JSONSerializer

@dataclass
class User:
    name: str
    username: str
    id: int
    groupname: str
    password: str
    state: str
    def __init__(self,id,username,name,groupname,password,state):
        self.id = id
        self.username = username
        self.name = name
        self.groupname = groupname
        self.password = password
        self.state = state
import pprint

class UserManager:
    def __init__(self):
        self.userlist = {}
        self.userid = 0

    def addUser(self,username,name,groupname,password,state):
        self.userlist[self.userid] = User(self.userid,username,name,groupname,password,state)
        self.userid = self.userid + 1
        return self.getUser(self.userid - 1)
    def getUser(self,id):
        pprint.pprint(self.userlist)
        print("ID:"  + str(id))
        return self.userlist[id]

    def getAllUsers(self):
        retval = []
        for userkey in self.userlist:
            retval.append(self.userlist[userkey])
        return retval


manager = UserManager()
manager.addUser("malcom2073","Mike","admin","12345","new")
manager.addUser("butterfly","Bob","users","54321","new")
class SingleUserMethod(MethodView):
    
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
        user = manager.getUser(int(userid))
        return {'id' : user.id, 'username':user.username,'name': user.name,'groupname':user.groupname,'password':user.password,'state':user.state},200

    def post(self,userid):
       
        userjson = request.get_json()
        user = manager.addUser(userjson['username'],userjson['name'],userjson['groupname'],userjson['password'],userjson['state'])
        return {'result':'success','newuser':{'id' : user.id, 'username':user.username,'name': user.name,'groupname':user.groupname,'password':user.password,'state':user.state}},200

    def put(self):
        """ Responds to PUT requests """
        return "Responding to a PUT request"

    def patch(self):
        """ Responds to PATCH requests """
        return "Responding to a PATCH request"

    def delete(self):
        """ Responds to DELETE requests """
        return "Responding to a DELETE request"



class UsersMethod(MethodView):
    
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
        users = manager.getAllUsers()
        return {'status':'success','users':JSONSerializer.serialize(users)},200

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
                        type: object
                        properties:
                            username:
                                type: string
                            name:
                                type: string
                            email:
                                type: string
                            password:
                                type: string
                            groupname:
                                type: string
                            state:
                                type: string
                                enum: [approved, pending, closed, new]
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
        user = manager.addUser(userjson['username'],userjson['name'],userjson['groupname'],userjson['password'],userjson['state'])
        return {'result':'success','newuser':{'id' : user.id, 'username':user.username,'name': user.name,'groupname':user.groupname,'password':user.password,'state':user.state}},200

    def put(self):
        """ Responds to PUT requests """
        return "Responding to a PUT request"

    def patch(self):
        """ Responds to PATCH requests """
        return "Responding to a PATCH request"

    def delete(self):
        """ Responds to DELETE requests """
        return "Responding to a DELETE request"

app.add_url_rule("/users/<userid>", view_func=SingleUserMethod.as_view("example_api"))
app.add_url_rule("/users", view_func=UsersMethod.as_view("example_apis"))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
