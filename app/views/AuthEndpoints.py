from flask import request, jsonify
from flask.views import MethodView
import db
import hashlib
from models.user import User
from models.group import Group
from models.usermetadata import UserMetadata
import pprint
from app import auth

class Authenticate(MethodView):

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

class Renew(MethodView):

    def post(self):
        
        userjson = request.get_json()
        dbsession = db.AppSession()
        group = dbsession.query(Group).filter(Group.name == userjson['groupname']).first()
        if group is None:
            # Invalid group!
            return {'status':'failure','error':'Invalid group name entered'}
        user = User(name=userjson['name'],username=userjson['username'],password=userjson['password'],email=userjson['email'],groups=[group])
        metalist = []
        if 'metadata' in userjson:
            # Metadata exists, so insert it into the metadata table
            for item in userjson['metadata']:
                if len(item.keys()) > 1:
                    # Bad!
                    return {'status':'failure','error':'Invalid metadata format'}
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
            return {'status':'failure','error':"Unable to add user: " + str(ex)}

        return {'status':'success','users':[user.as_obj()]},200