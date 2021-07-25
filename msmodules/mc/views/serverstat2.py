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
from ..models.msserverstat2 import MSServerStat2
class ServerStats2(MethodView):
#    @auth.jwt_private    
  def post(self):
    print("ServerStats2::post()")
    try:
      dbsession = db.AppSession()
      data = request.get_json()
      stat = MSServerStat2()
      stat.online = len(data['users'])
      stat.timestamp = data['timestamp']
      stat.cpusys10s = data['systime'][0]
      stat.cpusys1m = data['systime'][1]
      stat.cpusys15m = data['systime'][2]
      stat.cpuproc10s = data['proctime'][0]
      stat.cpuproc1m = data['proctime'][1]
      stat.cpuproc15m = data['proctime'][2]
      stat.tick10smin = data['ticktime10'][0]
      stat.tick10smed = data['ticktime10'][1]
      stat.tick10s95 = data['ticktime10'][2]
      stat.tick10smax = data['ticktime10'][3]
      stat.tick1mmin = data['ticktime60'][0]
      stat.tick1mmed = data['ticktime60'][1]
      stat.tick1m95 = data['ticktime60'][2]
      stat.tick1mmax = data['ticktime60'][3]
      stat.tps5s = data['tps_time'][0]
      stat.tps10s = data['tps_time'][1]
      stat.tps1m = data['tps_time'][2]
      stat.tps5m = data['tps_time'][3]
      stat.tps15m = data['tps_time'][4]
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
      stats = dbsession.query(MSServerStat2).order_by(MSServerStat2.timestamp.desc()).limit(1080).all()
      jsondoc = []
      for stat in stats:
        jsonobj = {}
        jsonobj['cpusys10s'] = stat.cpusys10s
        jsonobj['cpusys1m'] = stat.cpusys1m
        jsonobj['cpusys15m'] = stat.cpusys15m
        jsonobj['cpuproc10s'] = stat.cpuproc10s
        jsonobj['cpuproc1m'] = stat.cpuproc1m
        jsonobj['cpuproc15m'] = stat.cpuproc15m
        jsonobj['tick10smin'] = stat.tick10smin
        jsonobj['tick10smed'] = stat.tick10smed
        jsonobj['tick10s95'] = stat.tick10s95
        jsonobj['tick10smax'] = stat.tick10smax
        jsonobj['tick1mmin'] = stat.tick1mmin
        jsonobj['tick1mmed'] = stat.tick1mmed
        jsonobj['tick1m95'] = stat.tick1m95
        jsonobj['tick1mmax'] = stat.tick1mmax
        jsonobj['tps5s'] = stat.tps5s
        jsonobj['tps10s'] = stat.tps10s
        jsonobj['tps1m'] = stat.tps1m
        jsonobj['tps5m'] = stat.tps5m
        jsonobj['tps15m'] = stat.tps15m
        jsonobj['online'] = stat.online
#        jsonobj['ticktime'] = stat.ticktime
        jsonobj['timestamp'] = stat.timestamp
        jsondoc.append(jsonobj)
      return json.dumps(jsondoc)
    except Exception as e:
      print("Exception in ServerStats get")
      pprint.pprint(e)
      return{STATUS_KEY:FAIL_STR,ERROR_KEY:str(e)}

    return {STATUS_KEY:FAIL_STR,ERROR_KEY:"Unimplemented"}
