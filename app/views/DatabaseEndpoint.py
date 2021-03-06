from flask import request, jsonify
from flask.views import MethodView
import db
import hashlib
from models.user import User
from models.group import Group
from models.usermetadata import UserMetadata
import pprint
from app import auth

class DBCreate(MethodView):

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
        username  = userjson['username']
        password = userjson['password']
        print('User: ' + username,flush=True)
        print('Pass: ' + password,flush=True)
        dbsession = db.AppSession()
        user = dbsession.query(User).filter(User.username == username).first()
        pprint.pprint(user)
        dbsession.close()
        if user is None:
            print("No user",flush=True)
            return jsonify({'status':'failure','error':'invalid credentials'}),401
        if user is None or not user.password == password:
            print("Invalid user/pass",flush=True)
            return jsonify({'status':'failure','error':'invalid credentials'}),401
        if not user.validated:
            print("Un-validated user",flush=True)
            return jsonify({'status':'failure','error':'Account not yet activated'}),401
        session = request.cookies.get('session')
        m = hashlib.sha256()
        if session is None:
            session = auth.get_random_string(24)
        m.update(session.encode('utf-8'))

        # TODO: These are hardcoded at the moment.
        roleobj = {
            'user': username,
            'user_id': user.id,
            'roles': [
                'admin',
                'member-i',
                'member-iv'
            ],
            'session': m.hexdigest()
        }
        resp = jsonify({'status':'success','access_token':auth.encode_auth_token(roleobj)})
        resp.set_cookie("mspysid", value = session, httponly = True)
        return resp

class DBQuery(MethodView):

    @auth.jwt_private
    def post(self):
        jwt_token = auth.getJwt(request) # This is always valid due to @jwt_private decorator
        session = request.cookies.get('session')
        m = hashlib.sha256()
        if session is None:
            session = auth.get_random_string(24)
        m.update(session.encode('utf-8'))

        # TODO: These are hardcoded at the moment.
        jwt_token['session'] = m.hexdigest()
        resp = jsonify({'status':'success','access_token':auth.encode_auth_token(jwt_token)})
        resp.set_cookie("mspysid", value = session, httponly = True)
        return resp