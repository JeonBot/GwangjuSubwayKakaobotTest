#!/usr/bin/env python
# -*- coding: utf-8 -*-

# For data load
import urllib, json, datetime

from flask import Flask, request, jsonify
from gevent.wsgi import WSGIServer

app = Flask(__name__)

#@app.route('/')
#def hello():
#    return '안녕하세요?'

@app.route("/keyboard", methods=['GET', 'POST'])
#@app.route("/keyboard", methods=['GET'])
def keyboard():
    #if request.method == 'POST':
    #    print 'POST request'
    #else:
    #    print 'GET request'
    #return u"{'type':'buttons','buttons':['너는 누구니?', '사용법', '지하철']}"
    #return '{"type":"buttons", "buttons":["ch1","ch2","ch3" ]}'
    #return '{"type" : "buttons", "buttons" : ["어디?"]}'
    
    show_buttons = {
#                        "message": {
#                                        "text" : u"광주도시철도 카카오 플러스친구를 등록해주셔서 감사합니다.",
#                                        "photo": {
#                                                    "url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTbPTAm36d6ux4gAV0R0ag9XT9MhJWgOGY8PyvFCa6pgptyK2Vxfw",
#                                                    "width": 640,
#                                                    "height": 480
#                                        },            
#                        },
                        "type" : "buttons",
                        "buttons" : ["시작하기","사용법","개발사"]
                    }
    
    return jsonify(show_buttons)

@app.route("/message", methods=['POST'])
def message():
    dataReceive = request.get_json()
    content = dataReceive['content']

    if content == u"시작하기":
        show_buttons = {
                            "message": {
                                            "text": "안녕하세요? 어느 역에서 타시나요?"
                            },
#                                "type": {
#                                            "text"
#                            }
                            # 버튼은 한 화면에 3개씩 노출
                            "keyboard": {
                                            "type": "buttons",
                                            "buttons": ["녹동","소태","학동증심사입구","남광주","문화전당","금남로4가","금남로5가","양동시장","돌고개","농성","화정","운천","상무","쌍촌","김대중컨벤션센터","공항","송정공원","광주송정","도산","평동"]
                            }
#                            dataReceiveStation = request.get_json()
#                            contentStation = dataReceiveStation['content']
#                            if contentStation == u"녹동":
#                                show_buttons = {
#                                                    "message": {
#                                                                    "text": "thanx"
#                                                    }
#                                                }
                        }
    elif content == u"도움말":
        show_buttons = {
                            "message": {
                                            "text": "도움말인데 아직 내용은..."
                            }
                        }
    elif u"안녕" in content:
        show_buttons = {
                            "message": {
                                            "text": "안녕하세요! 반갑습니다!"
                            }
                        }
#    elif u"녹동" in content:
#        show_buttons = {
#                            "message": {
#                                            "text": "어디까지 가세요?"
#                            },
#                            "keyboard": {
#                                            "type": "buttons",
#                                            "buttons": ["녹동","소태","학동증심사","남광주","문화전당","금남로4가","금남로5가","양동시장","돌고개","농성","화정","운천","상무","쌍촌","김대중컨벤션센터","공항","송정공원","광주송정","도산","평동"]
#                            }
#                        }
    else:
        show_buttons = {
                            "message": {
                                            "text": "이해하지 못했어요."    
                            }
                        }
    return jsonify(show_buttons)

if __name__ == '__main__':
    http_server= WSGIServer(('', 3441), app)
    http_server.serve_forever()
