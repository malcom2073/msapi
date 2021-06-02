import pytest
import os
import sys
USER="malcom2073"
PASSWORD="12345"
SUCCESS_STR = 'success'
FAIL_STR = 'failure'
STATUS_KEY = 'status'
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
    db.initialize_empty_database(db)
    db.populate_sample_data(db)
#    clearDatabase()
#    loadDatabase('output.csv',False)
    return app.app.test_client()

#@pytest.fixture(autouse=True)
#def run_around_tests():
    # Code that will run before your test, for example:
#    db.populate_sample_data(db)
#    yield
#    files_before = # ... do something to check the existing files
#    # A test function will be run at this point
#    yield
#    # Code that will run after your test, for example:
#    files_after = # ... do something to check the existing files
#    assert files_before == files_after