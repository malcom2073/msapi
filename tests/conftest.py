import pytest
import os
import sys
USER = "admin"
PASSWORD = "testpassword"
sys.path.append("/home/mcarpenter/code/msapi")
import config
config.SQLALCHEMY_DATABASE_URI = "sqlite://"
import app
# Set sqlalchemy to use sqlite's in-memory database
#app.app.config['SECRET_KEY'] = "asfdsafdsadfsafdsadffdsa"
#app.app.config['SQLALCHEMY_URL'] = "sqlite://"
import db
@pytest.fixture
def client():
    #db.Model.metadata.create_all(db.engine)
    #db.session.commit()
#    sys.path.append("C:\\Users\\Michael\\code\\mikesshop.net")
#    sys.path.append("C:\\Users\\Michael\\code\\mikesshop.net\\python\\app")
#    sys.path.append("C:\\Users\\Michael\\code\\mikesshop.net\\python\\app\\models")
    print("Configuring client")
#    clearDatabase()
#    loadDatabase('output.csv',False)
    db.initialize_empty_database(db)
    return app.app.test_client()

