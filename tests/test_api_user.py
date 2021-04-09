from conftest import client
from conftest import PASSWORD
from conftest import USER
import json
import pprint
import datetime


data_createuser = {
  "email": "bob@asdf.com",
  "groupname": "Admin",
  "name": "bob",
  "password": "bobingabout123",
  "state": "new",
  "username": "bobinabout"
}
data_creategroup = {
    "name" : "Admin"
}

def test_groups_list_empty(client):
    print("*******************RUNNING TEST_BLOG_ADDPOST********************")
    rv = client.get("/groups")
    print("test")
    pprint.pprint(rv.data)
    jsonresponse = json.loads(rv.data)
    assert jsonresponse['status'] == "success"
    assert jsonresponse['groups'] == []


# Test inserting forums based on the forumindex variable above!
def test_user_list_empty(client):
    print("*******************RUNNING TEST_BLOG_ADDPOST********************")
    rv = client.get("/users")
    print("test")
    pprint.pprint(rv.data)
    jsonresponse = json.loads(rv.data)
    assert jsonresponse['status'] == "success"
    assert jsonresponse['users'] == []

#    assert False
    # Grab a token and cookie
#    rv = client.post('/auth/auth',json={ 'username': USER, 'password': PASSWORD })
#    jsonresponse = json.loads(rv.data)
#    assert jsonresponse['status'] == 'success'
#    assert 'access_token' in jsonresponse
#    accesstoken = jsonresponse['access_token']
#    assert 'Set-Cookie' in rv.headers
#    cookie = rv.headers['Set-Cookie']
#    rv = client.get('/userinfo',headers={'Set-Cookie':cookie,'Authorization':'Bearer ' + accesstoken})
#    pprint.pprint(rv.data)
#    jsonresponse = json.loads(rv.data)
#    assert 'data' in jsonresponse
#    assert 'name' in jsonresponse['data'] and jsonresponse['data']['name'] == USER
#    rv = client.post('/blog/addPost',
#        headers={'Set-Cookie':cookie,'Authorization':'Bearer ' + accesstoken},
#        json={'id':0,'title':'','date':'','content':'','tags':['new','blog','tech']})
#    jsonresponse = json.loads(rv.data)
#    pprint.pprint(jsonresponse)
#    assert 'status' in jsonresponse and jsonresponse['status'] == 'success'
    # We're good now to request to add forums!
    #for obj in forumindex:
    #    rv = client.post('/forum/addForum',
    #        headers={'Set-Cookie':cookie,'Authorization':'Bearer ' + accesstoken},
    #        json={'index':obj['id'],'title':obj['title'],'desc':obj['desc']})
    #    jsonresponse = json.loads(rv.data)
    #    assert 'status' in jsonresponse and jsonresponse['status'] == 'success'
    #    pprint.pprint(rv.data)
    ##assert False


def test_user_add_badgroup(client):
    print("*******************RUNNING TEST_BLOG_ADDPOST********************")
    rv = client.post('/users',json=data_createuser)
    jsonresponse = json.loads(rv.data)
    pprint.pprint(rv.data)
    assert jsonresponse['status'] == "failure"
#    assert jsonresponse['result']['email'] == data_createuser['email']
#    assert False

def test_group_add_good(client):
    print("*******************RUNNING test_group_add_good********************")
    rv = client.post('/groups',json=data_creategroup)
    jsonresponse = json.loads(rv.data)
    pprint.pprint(rv.data)
    assert jsonresponse['status'] == "success"
    rv = client.get("/groups")
    pprint.pprint(rv.data)
    jsonresponse = json.loads(rv.data)
    assert jsonresponse['status'] == "success"
    assert len(jsonresponse['groups']) > 0
    assert jsonresponse['groups'][0]['name'] == data_creategroup['name']
#    assert jsonresponse['result']['email'] == data_createuser['email']
#    assert False



def test_group_add_bad_duplicate(client):
    print("*******************RUNNING test_group_add_bad_duplicate********************")
    rv = client.post('/groups',json=data_creategroup)
    jsonresponse = json.loads(rv.data)
    pprint.pprint(rv.data)
    assert jsonresponse['status'] == "failure"
#    assert jsonresponse['result']['email'] == data_createuser['email']
#    assert False

def test_user_add_good(client):
    print("*******************RUNNING test_user_add_good********************")
    #test_group_add_good(client)
    rv = client.post('/users',json=data_createuser)
    jsonresponse = json.loads(rv.data)
    pprint.pprint(rv.data)
    assert jsonresponse['status'] == "success"
    rv = client.get("/users")
    pprint.pprint(rv.data)
    jsonresponse = json.loads(rv.data)
    assert jsonresponse['status'] == "success"
    assert len(jsonresponse['users']) > 0
    assert jsonresponse['users'][0]['name'] == data_createuser['name']
    assert jsonresponse['users'][0]['email'] == data_createuser['email']
    assert jsonresponse['users'][0]['password'] == data_createuser['password']
#    assert jsonresponse['users'][0]['state'] == data_createuser['state']
    assert jsonresponse['users'][0]['username'] == data_createuser['username']
    groupname_found = False
    for group in jsonresponse['users'][0]['groups']:
        if group['name'] == data_createuser['groupname']:
            groupname_found = True
    assert groupname_found
#    assert jsonresponse['']

#    assert jsonresponse['result']['email'] == data_createuser['email']
#    assert False

def test_user_add_duplicate(client):
    print("*******************RUNNING test_user_add_duplicate********************")
    #test_group_add_good(client)
    #test_user_add_good(client)
    rv = client.post('/users',json=data_createuser)
    jsonresponse = json.loads(rv.data)
    pprint.pprint(rv.data)
    assert jsonresponse['status'] == "failure"
#    assert jsonresponse['result']['email'] == data_createuser['email']
#    assert False
