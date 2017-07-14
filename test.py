#!/usr/bin/env python
# -*- coding: utf-8 -*-

# For data load
import urllib, json, datetime

from flask import Flask, request, jsonify
from gevent.wsgi import WSGIServer

app = Flask(__name__)

@app.route('/')
def hello():
    return "안녕하세요?"
def getStationID(stationName):
    try:
        stationIDdict =  {
            u'녹동': 100,
            u'소태': 101,
            u'학동증심사입구': 102,
            u'학동증심사': 102,
            u'학동증':102,
            u'학동':102,
            u'남광주': 103,
            u'문화전당(구도청)': 104,
            u'문화전당': 104,
            u'문화전':104,
            u'문화': 104,
            u'금남로4가' : 105,
            u'금남4':105,
            u'금4':105,
            u'금남고5가' : 106,
            u'금남5':106,
            u'금5':106,
            u'양동시장' : 107,
            u'돌고개' : 108,
            u'농성' : 109,
            u'화정' : 110,
            u'쌍촌' : 111,
            u'운천' : 112,
            u'상무' : 113,
            u'김대중컨벤션센터(마륵)' : 114,
            u'김대중': 114,
            u'김대':114,
            u'공항' : 115,
            u'송정공원' : 116,
            u'송정':116,
            u'광주송정역' : 117,
            u'광주송정':117,
            u'광주':117,
            u'도산' : 118,
            u'평동' : 119,
        }[stationName]
        return stationIDdict
    except:
        print "Exception non existing Station Name: ", stationName
        return None

@app.route("/keyboard", methods=["GET", "POST"])
#@app.route("/keyboard", methods=["GET"])
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
                        "type": "buttons",
                        "buttons": ["시작하기","사용법","개발사"]
                    }
    
    return jsonify(show_buttons)

@app.route("/message", methods=["POST"])
def message():
    dataReceive = request.get_json()
    content = dataReceive['content']

    if content == u"시작하기":
        show_buttons = {
                            "message": {
                                            "text": "어디에서 탑승하시나요? 옆으로 쓸어 넘겨 출발지를 찾아보세요."
                            },
#                                # 말로 받기?
#                                "type": "text"
                            # 버튼은 한 화면에 3개씩 노출
                            "keyboard": {
                                            "type": "buttons",
                                            "buttons": ["녹동에서","소태에서","학동증심사입구에서","남광주에서","문화전당에서","금남로4가에서","금남로5가에서","양동시장에서","돌고개에서","농성에서","화정에서","운천에서","상무에서","쌍촌에서","김대중컨벤션센터에서","공항에서","송정공원에서","광주송정에서","도산에서","평동에서"]
                            }
                        }
#        # 이렇겐 안되는데...
#        dataReceiveStation = request.get_json()
#        contentStation = dataReceiveStation['content']
#        if contentStation == u"녹동":
#                show_buttons = {
#                                    "message": {
#                                                    "text": "thanx"
#                                    }
#                                }
                        
    elif content == u"사용법":
        show_buttons = {
                            "message": {
                                            "text": "도움말인데 아직 내용은..."
                            },
                            "keyboard": {
                                            "type": "buttons",
                                            "buttons": ["시작하기","사용법","개발사"]
                            }

                        }
    elif u"안녕" in content:
        show_buttons = {
                            "message": {
                                            "text": "안녕하세요! 반갑습니다!"
                            }
                        }
#    # 이렇게 놓으면 가는 녹동인지 오는 녹동인지 모른다.
#    elif u"녹동" in content:
#        show_buttons = {
#                            "message": {
#                                            "text": "어디까지 가세요?"
#                            },
#                            "keyboard": {
#                                            "type": "buttons",
#                                            "buttons": ["녹동으로","소태로","학동증심사입구로","남광주로","문화전당으로","금남로4가로","금남로5가로","양동시장으로","돌고개로","농성으로","화정으로","운천으로","상무로","쌍촌으로","김대중컨벤션센터로","공항으로","송정공원으로","광주송정으로","도산으로","평동으로"]
#                            }
#                        }
    elif u"녹동에서" in content:
        show_buttons = {
                            "message": {
                                            "text": "어디까지 가시나요?"
                            },
                            "keyboard": {
                                            "type": "buttons",
                                            "buttons": ["녹동으로","소태로","학동증심사입구로","남광주로","문화전당으로","금남로4가로","금남로5가로","양동시장으로","돌고개로","농성으로","화정으로","운천으로","상무로","쌍촌으로","김대중컨벤션센터로","공항으로","송정공원으로","광주송정으로","도산으로","평동으로"]
                            }
                        }
    elif u"소태로" in content:
        show_buttons = {
                            "message": {
                                            "text": "현재 몇분 남았습니다"
                            },
                            "keyboard": {
                                            "type": "buttons",
                                            "buttons": ["시작하기","사용법","개발사"]
                            }
                        }
    elif u"개발사" in content:
        show_buttons = {
                            "message": {
                                            "text": "KETI 전자부품연구원\n임베디드 & SW 연구센터", 
                                            "photo": {
                                                        "url": "http://www.keti.re.kr/_upload/editor/2016/12/09/recruit_main-1481273868_5aeb7d6cabb864d7c90a25ca125a930d.bmp",
                                                        "width": 640,
                                                        "height": 480
                                            }
                            },
                            "keyboard": {
                                            "type": "buttons",
                                            "buttons": ["시작하기","사용법","개발사"]
                            }                            
                        }
    else:        
        show_buttons = {
                            "message": {
                                            "text": "이해하지 못했어요. 무엇을 할까요?"    
                            },
                            "keyboard": {
                                            "type": "buttons",
                                            "buttons": ["시작하기","사용법","개발사"]
                            }

                        }
    return jsonify(show_buttons)

if __name__ == '__main__':
    http_server= WSGIServer(('', 3441), app)
    http_server.serve_forever()
