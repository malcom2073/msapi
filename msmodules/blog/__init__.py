#module_bp.add_url_rule("/api/auth/authenticate", view_func=Authenticate.as_view("example_apisauth"))
#module_bp.add_url_rule("/api/auth/renew", view_func=Renew.as_view("example_apisauthrenew"))



from flask import Blueprint, render_template, Flask, jsonify, request,send_file
import pprint
import hashlib
import random
import string
import datetime
import jwt
import sys # For sys.stdout.flush()
#from PIL import Image
#from util import getJwt, getAuthToken
from app.auth import jwt_private
module_bp = Blueprint('blog_bp', __name__)
module_prefix = '/blog'
#import db
#import models
#from app.models.user import User
#from app.models.group import Group
#from app.models import userprofilefield as UserProfileField
#from modules.blog.python.models.msblogpost import MSBlogPost
import app
import os
from sqlalchemy import and_, or_, not_
from .views.postcollection import PostCollection
from .views.postresource import PostResource
from .models.msblogpost import MSBlogPost
module_bp.add_url_rule("/posts", view_func=PostCollection.as_view("example_apisauth"))
module_bp.add_url_rule("/posts/<postid>", view_func=PostResource.as_view("example_apisauth2"))

PostResource
# Should there be a standard set of module endpoints?
# Something like: /getVersion, /getInfo, /getAuthor?

""" @module_bp.route('/addPost',methods=['POST'])
@jwt_private
def addPost():
    jwt = getJwt(request)
    post_data = request.get_json()
    pprint.pprint(post_data)
    #print('Index: ' + str(post_data.get('id')))
    print('Title: ' + post_data.get('title'))
    print('Date: ' + str(post_data.get('date')))
    print('Content: ' + post_data.get('content'))
    sys.stdout.flush()
    blogpostid = 0
    try:
        dbsession = db.Session()
        blogpost = MSBlogPost(user_id=post_data.get('user_id'),title=post_data.get('title'),timestamp=post_data.get('date'),content=post_data.get('content'),published=False)
        dbsession.add(blogpost)
        dbsession.commit()
        blogpostid = blogpost.id
        dbsession.close()
    except Exception as e:
        return jsonify({'status':'error','error':str(e)})
    return jsonify({'status':'success','postid':blogpostid})


@module_bp.route('/publishPost',methods=['POST'])
@jwt_private
def publishPost():
    jwt = getJwt(request)
    post_data = request.get_json()
    #pprint.pprint(post_data)
    #print('Index: ' + str(post_data.get('id')))
    print('ID: ' + str(post_data.get('postid')))
    postid = post_data.get('postid')
    published = post_data.get('published')
    #print('Content: '.encode('utf-8') + post_data.get('content').encode('utf-8'))
    #sys.stdout.flush()
    dbsession = db.Session()
    try:
        postlist = dbsession.query(MSBlogPost).filter(MSBlogPost.id == postid).all()
        singlepost = postlist[0]
        singlepost.published = published
        #singlepost.title = post_data.get('title')
        #singlepost.content = post_data.get('content')
        dbsession.commit()
        dbsession.close()
    except Exception as e:
        dbsession.rollback()
        dbsession.close()
        return jsonify({'status':'error','error':str(e)})
    return jsonify({'status':'success'})



@module_bp.route('/editPost',methods=['POST'])
@jwt_private
def editPost():
    jwt = getJwt(request)
    post_data = request.get_json()
    #pprint.pprint(post_data)
    #print('Index: ' + str(post_data.get('id')))
    print('Title: ' + post_data.get('title'))
    print('ID: ' + str(post_data.get('id')))
    postid = post_data.get('id')
    print('Content: '.encode('utf-8') + post_data.get('content').encode('utf-8'))
    sys.stdout.flush()
    dbsession = db.Session()
    try:
        postlist = dbsession.query(MSBlogPost).filter(MSBlogPost.id == postid).all()
        singlepost = postlist[0]
        singlepost.title = post_data.get('title')
        singlepost.content = post_data.get('content')
        singlepost.timestamp = post_data.get('timestamp')
        dbsession.commit()
        dbsession.close()
    except Exception as e:
        dbsession.rollback()
        dbsession.close()
        return jsonify({'status':'error','error':str(e)})
    return jsonify({'status':'success'})


@module_bp.route('/upload',methods=['PUT'])
@jwt_private
def upload():
    print("/upload called")
    sys.stdout.flush()
    pprint.pprint(request.files)
    pprint.pprint(request)
    for f in request.files:
        print("File: " + f)
        pprint.pprint(request.files.get(f))
        filestor = request.files.get(f)
        filestor.save(os.path.join('..','uploads','upload',f))
        size = 128, 128
        im = Image.open(os.path.join('..','uploads','upload',f))
        im.thumbnail(size)
        if im.mode in ("RGBA", "P"):
            im = im.convert("RGB") 
        im.save(os.path.join('..','uploads','upload',"thumbnail." + f), "JPEG")
    formdict = request.form.to_dict()
    pprint.pprint(formdict)
    #pprint.pprint(formdict['file'])
    #pprint.pprint(formdict['image[image]'])
    sys.stdout.flush()
    jwt = getJwt(request)
    post_data = request.get_json()
    pprint.pprint(post_data)
    return jsonify({'status':'success','path':'/upload/' + "thumbnail." + f})
    #pprint.pprint(post_data)
    #print('Index: ' + str(post_data.get('id')))
    print('Title: ' + post_data.get('title'))
    print('ID: ' + str(post_data.get('id')))
    postid = post_data.get('id')
    print('Content: '.encode('utf-8') + post_data.get('content').encode('utf-8'))
    sys.stdout.flush()
    dbsession = db.Session()
    try:
        postlist = dbsession.query(MSBlogPost).filter(MSBlogPost.id == postid).all()
        singlepost = postlist[0]
        singlepost.title = post_data.get('title')
        singlepost.content = post_data.get('content')
        dbsession.commit()
        dbsession.close()
    except Exception as e:
        dbsession.rollback()
        dbsession.close()
        return jsonify({'status':'error','error':str(e)})
    return jsonify({'status':'success'})


@module_bp.route('/getPosts',methods=['GET'])
def getPosts():
    jwt = getJwt(request)
    print("JWT!!!")
    pprint.pprint(jwt)
    print("JWT!!!")
    print(jwt)
    uid = None
    if jwt:
        uid = jwt['user_id']
    print("User ID: " + str(uid))
#    jwt = getJwt(request)
#    post_data = request.get_json()
#    pprint.pprint(post_data)
    #print('Index: ' + str(post_data.get('id')))
#    print('Last: ' + str(post_data.get('last')))
    sys.stdout.flush()
    try:
        dbsession = db.Session()
        #filter(or_(User.name == 'ed', User.name == 'wendy'))
        #postlist = dbsession.query(MSBlogPost).filter((MSBlogPost.published == True) | (MSBlogPost.published == False & MSblogPost.user = )).order_by(MSBlogPost.timestamp.desc()).all()
        postlist = None
        if uid is not None:
            postlist = dbsession.query(MSBlogPost).filter(or_(MSBlogPost.published == True,MSBlogPost.user_id == uid)).order_by(MSBlogPost.timestamp.desc()).all()
        else:
            postlist = dbsession.query(MSBlogPost).filter(MSBlogPost.published == True).order_by(MSBlogPost.timestamp.desc()).all()
        jsonresponse = jsonify({'status':'success','data': postlist})
        dbsession.close()
        print("Postcount: " + str(len(postlist)))
        sys.stdout.flush()

        if postlist is None or len(postlist) == 0:
            print("No posts")
            return jsonify({'status':'error','error':'No Posts'})
        return jsonresponse
    except Exception as e:
        return jsonify({'status':'error','error':str(e)})
    return jsonify({'status':'success'})



@module_bp.route('/getPost',methods=['GET'])
def getPost():
#    jwt = getJwt(request)
    postid = int(request.args.get('postid'))
#    pprint.pprint(post_data)
    #print('Index: ' + str(post_data.get('id')))
#    sys.stdout.flush()
    try:
        dbsession = db.Session()
        postlist = dbsession.query(MSBlogPost).filter(MSBlogPost.id == postid).all()
        jsonresponse = jsonify({'status':'success','data': postlist[0]})
        dbsession.close()
        if postlist is None or len(postlist) == 0:
            print("No posts")
            return jsonify({'status':'error','error':'No Posts'})
        return jsonresponse
    except Exception as e:
        return jsonify({'status':'error','error':str(e)})
    return jsonify({'status':'success'})



 """