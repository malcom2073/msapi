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
      chat.description = data['description']
      chat.uuid = data['uuid']
      chat.msgtype = data['msgtype']
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
      chats = dbsession.query(MSServerChat).filter(MSServerChat.source != server).filter(MSServerChat.timestamp > timestamp).order_by(MSServerChat.timestamp.desc()).limit(50).all()
      retval = {}
      jsondoc = []
      lasttimestamp = timestamp

      first = True
      # Remember, these are in backwards order! This is so our limit() call works properly.
      for chat in chats:
        if first:
          lasttimestamp = chat.timestamp
          first = False
        jsonobj = {}
        jsonobj['username'] = chat.username
        jsonobj['text'] = chat.text
        jsonobj['description'] = chat.description
        jsonobj['uuid'] = chat.uuid
        jsonobj['msgtype'] = chat.msgtype
        jsonobj['timestamp'] = chat.timestamp
        jsonobj['server'] = chat.source
        jsondoc.insert(0,jsonobj)
      retval['chat'] = jsondoc
      retval['last'] = lasttimestamp
      return json.dumps(retval)
    except Exception as e:
      print("Exception in ServerChat get")
      pprint.pprint(e)
      return{STATUS_KEY:FAIL_STR,ERROR_KEY:str(e)}

    return {STATUS_KEY:FAIL_STR,ERROR_KEY:"Unimplemented"}
