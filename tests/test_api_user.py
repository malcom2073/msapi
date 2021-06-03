from conftest import client
from conftest import PASSWORD
from conftest import USER
from conftest import SUCCESS_STR
from conftest import FAIL_STR
from conftest import STATUS_KEY
from conftest import ERROR_KEY
import json
import pprint
import datetime

    
data_createuser = {
  "email": "bob@asdf.com",
  "groupname": "Users",
  "name": "bob",
  "password": "bobingabout123",
  "state": "new",
  "username": "bobinabout",
  "metadata": [
      {
          "city":"westminster"
      },
      {
          "state":"maryland"
      }
  ]
}
data_creategroup = {
    "name" : "Users"
}




def test_user_add_badgroup(client):
    print("*******************RUNNING TEST_BLOG_ADDPOST********************")
    headers=get_valid_token(client)
    rv = client.post('/api/users',json=data_createuser,headers=headers)
    jsonresponse = json.loads(rv.data)
    pprint.pprint(rv.data)
    assert jsonresponse[STATUS_KEY] == FAIL_STR

def test_group_add_good(client):
    print("*******************RUNNING test_group_add_good********************")
    headers = get_valid_token(client)
    rv = client.post('/api/groups',json=data_creategroup,headers=headers)
    jsonresponse = json.loads(rv.data)
    pprint.pprint(rv.data)
    assert jsonresponse[STATUS_KEY] == SUCCESS_STR
    rv = client.get("/api/groups",headers=headers)
    pprint.pprint(rv.data)
    jsonresponse = json.loads(rv.data)
    assert jsonresponse[STATUS_KEY] == SUCCESS_STR
    assert len(jsonresponse['groups']) > 0
    found = False
    for group in jsonresponse['groups']:
        if group['name'] == data_creategroup['name']:
            found = True
    assert found
#    assert jsonresponse['groups'][0]['name'] == data_creategroup['name']
#    assert jsonresponse['result']['email'] == data_createuser['email']
#    assert False



def test_group_add_bad_duplicate(client):
    print("*******************RUNNING test_group_add_bad_duplicate********************")
    rv = client.post('/api/groups',json=data_creategroup)
    jsonresponse = json.loads(rv.data)
    pprint.pprint(rv.data)
    assert jsonresponse[STATUS_KEY] == FAIL_STR
#    assert jsonresponse['result']['email'] == data_createuser['email']
#    assert False

def test_auth_endpoints(client):

    rv = client.get('/api/users')
    jsonresponse = json.loads(rv.data)
    assert (jsonresponse[STATUS_KEY] == FAIL_STR and jsonresponse[ERROR_KEY] == 'Null session')

    rv = client.get('/api/groups')
    jsonresponse = json.loads(rv.data)
    assert (jsonresponse[STATUS_KEY] == FAIL_STR and jsonresponse[ERROR_KEY] == 'Null session')


def get_valid_token(client,username=USER,password=PASSWORD):
    # Authenticate to get our token
    rv = client.post('/api/auth/authenticate',json={ 'username': username, 'password': password })
    jsonresponse = json.loads(rv.data)

    # Verify the password worked and we have a token
    assert jsonresponse[STATUS_KEY] == SUCCESS_STR
    assert 'access_token' in jsonresponse
    accesstoken = jsonresponse['access_token']
    assert 'Set-Cookie' in rv.headers
    cookie = rv.headers['Set-Cookie']
    return {'Set-Cookie':cookie,'Authorization':'Bearer ' + accesstoken}

def test_authenticate(client):
    # Test invalid authentication
    rv = client.post('/api/auth/authenticate',json={ 'username': 'wrong', 'password': 'bad' })
    jsonresponse = json.loads(rv.data)
    assert jsonresponse[STATUS_KEY] == FAIL_STR

    rv = client.post('/api/auth/authenticate',json={ 'username': USER, 'password': 'bad' })
    jsonresponse = json.loads(rv.data)
    assert jsonresponse[STATUS_KEY] == FAIL_STR

    header = get_valid_token(client)
    assert 'Set-Cookie' in header and 'Authorization' in header




def test_user_add_good(client):
    test_group_add_good(client)
    print("*******************RUNNING test_user_add_good********************")

    # Verify we get a null session, since we're not passing in a valid token
    rv = client.get('/api/users')
    jsonresponse = json.loads(rv.data)
    assert (jsonresponse[STATUS_KEY] == FAIL_STR and jsonresponse[ERROR_KEY] == 'Null session')

    headers = get_valid_token(client)

    # Create a new user
    rv = client.post('/api/users',json=data_createuser,headers=headers)
    jsonresponse = json.loads(rv.data)
    print("post to user create result:",flush=True)
    pprint.pprint(jsonresponse)

    # Verify it succeeds
    assert jsonresponse[STATUS_KEY] == SUCCESS_STR

    # Grab the new user from the users endpoint, and validate that it created properly
    newuserid = jsonresponse['users'][0]['id']
    rv = client.get("/api/users/" + str(newuserid),headers=headers)
    jsonresponse = json.loads(rv.data)

    assert jsonresponse[STATUS_KEY] == SUCCESS_STR
    assert len(jsonresponse['users']) == 1
    assert jsonresponse['users'][0]['username'] == data_createuser['username']
    assert jsonresponse['users'][0]['email'] == data_createuser['email']
    assert jsonresponse['users'][0]['password'] == data_createuser['password']
    assert jsonresponse['users'][0]['name'] == data_createuser['name']

    groupname_found = False
    for group in jsonresponse['users'][0]['groups']:
        if group['name'] == data_createuser['groupname']:
            groupname_found = True
    assert groupname_found

    for pre_usermeta in data_createuser['metadata']:        
        found = False
        for usermeta in jsonresponse['users'][0]['usermeta']:
            if usermeta['key'] in pre_usermeta and usermeta['value'] == pre_usermeta[usermeta['key']]:
                found = True
        assert found

def test_user_add_duplicate(client):
    print("*******************RUNNING test_user_add_duplicate********************")
    #test_group_add_good(client)
    #test_user_add_good(client)
    rv = client.post('/api/users',json=data_createuser)
    jsonresponse = json.loads(rv.data)
    pprint.pprint(rv.data)
    assert jsonresponse[STATUS_KEY] == FAIL_STR
#    assert jsonresponse['result']['email'] == data_createuser['email']
#    assert False


def test_user_login_not_validated(client):
    test_user_add_good(client)
    # Try to access a user that is not validated
    rv = client.post('/api/auth/authenticate',json={ 'username': data_createuser['username'], 'password': data_createuser['password'] })
    jsonresponse = json.loads(rv.data)

    # Grab real credentials
    assert jsonresponse[STATUS_KEY] == FAIL_STR
    headers = get_valid_token(client)

    # Get our test user that we added
    rv = client.get('/api/users',headers=headers)
    jsonresponse = json.loads(rv.data)
    assert jsonresponse[STATUS_KEY] == SUCCESS_STR

    founduser = None
    for user in jsonresponse['users']:
        if user['username'] == data_createuser['username']:
            founduser = user
            break

    assert founduser
    assert 'validated' in founduser and founduser['validated'] == False

    # Validate the user
    rv = client.patch("/api/users/" + str(founduser['id']),json={'validated':True},headers=headers)
    jsonresponse = json.loads(rv.data)
    assert jsonresponse[STATUS_KEY] == SUCCESS_STR
    assert len(jsonresponse['users']) == 1
    assert 'validated' in jsonresponse['users'][0] and jsonresponse['users'][0]['validated'] == True



