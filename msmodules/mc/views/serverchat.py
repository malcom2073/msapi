from msmodules.mc.models.msserverstat import MSServerStat
from flask.views import MethodView
from flask import request, jsonify
import db
from models.user import User
from models.group import Group
import json
import pprint
from app import auth
from app import SUCCESS_STR
from app import FAIL_STR
from app import STATUS_KEY
from app import ERROR_KEY
from PIL import Image
import os

import sys
from sqlalchemy import and_, or_, not_
from ..models.msserverchat import MSServerChat
class ServerChat(MethodView):

#    @auth.jwt_private    
  def post(self):
    print("ServerChat::post()")
    try:
      dbsession = db.AppSession()
      data = request.get_json()
      chat = MSServerChat()
      chat.username = data['username']
      chat.text = data['text']
      chat.uuid = data['uuid']
      chat.timestamp = data['timestamp']
      chat.source = data['server']
      dbsession.add(chat)
      dbsession.commit()
    except Exception as e:
      print("Exception submitting chat event")
      print(e)
      return jsonify({STATUS_KEY:FAIL_STR,ERROR_KEY:str(e)})
#    return {STATUS_KEY:FAIL_STR,ERROR_KEY:"Unimplemented"}
    return {STATUS_KEY:SUCCESS_STR}
  def get(self):
    print("ServerChat::get()")
    # Get all the chats SINCE the last timstamp
    timestamp = int(request.args.get('timestamp'))
    server = request.args.get('server')
    try:
      dbsession = db.AppSession()
      chats = dbsession.query(MSServerChat).filter(MSServerChat.source == server).filter(MSServerChat.timestamp < timestamp).order_by(MSServerChat.timestamp.desc()).limit(1080).all()
      retval = {}
      retval['last'] = str(timestamp)
      jsondoc = []
      for chat in chats:
        jsonobj = {}
        jsonobj['username'] = chat.username
        jsonobj['text'] = chat.text
        jsonobj['uuid'] = chat.uuid
        jsonobj['timestamp'] = chat.timestamp
        jsonobj['server'] = chat.source
        jsondoc.append(jsonobj)
      retval['chat'] = jsondoc
      return json.dumps(retval)
    except Exception as e:
      print("Exception in ServerChat get")
      pprint.pprint(e)
      return{STATUS_KEY:FAIL_STR,ERROR_KEY:str(e)}

    return {STATUS_KEY:FAIL_STR,ERROR_KEY:"Unimplemented"}
