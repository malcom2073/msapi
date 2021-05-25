from flask import Flask, jsonify, request
from flask.views import MethodView
import json
import config
config.SQLALCHEMY_DATABASE_URI = "sqlite:///test.sqlite3"

import app
app.app.config['SECRET_KEY'] = "asfdsafdsadfsafdsadffdsa"
#app.config['SQLALCHEMY_URL'] = "sqlite:///test.sqlite3"

import pprint
#app.config['SWAGGER'] = {}
#app.config['SWAGGER']['openapi'] = '3.0.2'
from flasgger import Swagger
print("Running")

import db
db.initialize_empty_database(db)
db.populate_sample_data(db)

from models.user import User
from models.group import Group
from models.usergroup import UserGroup
from dataclasses import dataclass
from dataclasses_serialization.json import JSONSerializer

#db.Model.metadata.create_all(db.engine)
#for tbl in reversed(db.Model.metadata.sorted_tables):
#    try:    
#    tbl.drop(db.engine)
#    except:
#        print("unable to drop")
#        pass
#db.mainsession.commit()


swagger_config = {
    "headers": [],
    "openapi": "3.0.2",
    "components": {
        'schemas': {
            'Group': {
                'type': 'object',
                'properties': {
                    'id': {
                        'type': 'integer',
                        'format': 'int64'
                    },
                    'name': {
                        'type': 'string'
                    }
                }
            },
            'User': {
                'type': 'object',
                'properties': {
                    'id': {
                        'type': 'integer',
                        'format': 'int64'
                    },
                    'group': {
                        '$ref': '#/components/schemas/Group'
                    },
                    'name': {
                        'type': 'string'
                    },
                    'username': {
                        'type': 'string'
                    },
                    'groupname': {
                        'type': 'string'
                    },
                    'password': {
                        'type': 'string'
                    },
                    'state': {
                        'enum': ['approved', 'pending', 'closed', 'new'],
                        'type': 'string'
                    }
                }
            }
        }
    },
    "title": "MikesShop API",
    "version": 'v1.0.0',
    "termsOfService": "",
    "static_url_path": "/characteristics/static",
    "swagger_ui": True,
    "description": "",
}

swagger = Swagger(app.app, config=swagger_config, merge=True)



if __name__ == '__main__':
    app.app.run(host='0.0.0.0', port=5000, debug=True)
