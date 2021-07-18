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
from ..models.msserverstat import MSServerStat
class ServerStats(MethodView):

#    @auth.jwt_private    
  def post(self):
    print("ServerStats::post()")
    try:
      dbsession = db.AppSession()
      data = request.get_json()
      stat = MSServerStat()
      stat.online = len(data['users'])
      stat.tps = data['tps']
      stat.ticktime = data['ticktime']
      stat.timestamp = data['timestamp']
      dbsession.add(stat)
      dbsession.commit()
    except Exception as e:
      print("Exception submitting serverstat")
      print(e)
      return jsonify({STATUS_KEY:FAIL_STR,ERROR_KEY:str(e)})
#    return {STATUS_KEY:FAIL_STR,ERROR_KEY:"Unimplemented"}
    return {STATUS_KEY:SUCCESS_STR}
  def get(self):
    print("ServerStats::get()")
    try:
      dbsession = db.AppSession()
      stats = dbsession.query(MSServerStat).order_by(MSServerStat.timestamp.desc()).limit(1080).all()
      jsondoc = []
      for stat in stats:
        jsonobj = {}
        jsonobj['tps'] = stat.tps
        jsonobj['online'] = stat.online
        jsonobj['ticktime'] = stat.ticktime
        jsonobj['timestamp'] = stat.timestamp
        jsondoc.append(jsonobj)
      return json.dumps(jsondoc)
    except Exception as e:
      print("Exception in ServerStats get")
      pprint.pprint(e)

    return {STATUS_KEY:FAIL_STR,ERROR_KEY:"Unimplemented"}
