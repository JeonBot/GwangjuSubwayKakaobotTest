#!/usr/bin/env python
# -*- coding: utf-8 -*-

# For data load
import urllib, json, datetime, requests, random, time

from flask import Flask, request, jsonify, Response, send_from_directory
from gevent.wsgi import WSGIServer

app = Flask(__name__)

# Variables
#global contentTO
#global contentFROM
FROM = ["녹동에서","소태에서","학동증심사입구에서","남광주에서","문화전당에서","금남로4가에서","금남로5가에서","양동시장에서","돌고개에서","농성에서","화정에서","운천에서","상무에서","쌍촌에서","김대중컨벤션센터에서","공항에서","송정공원에서","광주송정에서","도산에서","평동에서"]
TO = ["녹동까지","소태까지","학동증심사입구까지","남광주까지","문화전당까지","금남로4가까지","금남로5가까지","양동시장까지","돌고개까지","농성까지","화정까지","운천까지","상무까지","쌍촌까지","김대중컨벤션센터까지","공항까지","송정공원까지","광주송정까지","도산까지","평동까지"]
DEFAULT = ["시작하기","사용법","개발사"]
STATIONDIC = {u'녹동에서': 100, u'녹동까지':100, u'소태에서': 101, u'소태까지':101, u'학동증심사입구에서': 102, u'학동증심사입구까지':102, u'남광주에서': 103, u'남광주까지':103, u'문화전당에서': 104, u'문화전당까지':104, u'금남로4가에서': 105, u'금남로4가까지':105, u'금남로5가에서': 106, u'금남로5가까지':106, u'양동시장에서': 107, u'양동시장까지':107, u'돌고개에서': 108, u'돌고개까지':108, u'농성에서': 109, u'농성까지':109, u'화정에서': 110, u'화정까지':110, u'운천에서': 111, u'운천까지':111, u'상무에서': 112, u'상무까지':112, u'쌍촌에서': 113, u'쌍촌까지':113, u'김대중컨벤션센터에서': 114, u'김대중컨벤션센터까지':114, u'공항에서': 115, u'공항까지':115, u'송정공원에서': 116, u'송정공원까지':116, u'광주송정에서': 117, u'광주송정까지':117, u'도산에서': 118, u'도산까지':118, u'평동에서': 119, u'평동까지':119}
RESTART = ["처음으로", "다시시작하기"]

# StationName to Integer
def getStationID(stationName):
    try:
        stationIDdict = STATIONDIC[stationName]
        return stationIDdict
    except:
        print "Exception non existing Station Name: ", stationName
        return None

@app.route('/')
def Metro():
    url = 'http://energy.openlab.kr:3003'
    u = urllib.urlopen(url)
    data = u.read()

    j=json.loads(data)

    subway = j["subway"]
    first_subway = subway[0]
    second_subway = subway[1]
#    print "subway location?"
#    print subway_arr["Location"]
#    print "\n"
    pos = first_subway["Location"]
    
    return first_subway["Location"]

#@app.route('/')
#def hello():
#    return "안녕하세요?"

@app.route('/keyboard', methods=['GET'])
def keyboard():
#    # 바로 시작
#    # content = request.get_json()    
#    show_buttons = json.dumps({
#                    # 버튼은 한 화면에 3개씩 노출
#                    # 최대 10개 노출 가능하다는데 알 방법이 없음
#                                "type": "buttons",
#                                "buttons": TO
#                    })
#    return Response(show_buttons, mimetype='application/json')
    # 첫 화면을 버튼으로.
    show_buttons = json.dumps({
                                "type": "buttons",
                                "buttons": DEFAULT
                    })
    return Response(show_buttons, mimetype='application/json')

#    # 첫 화면을 아무말로.
#    response = json.dumps({"type" : "text"})
#    return Response(response, mimetype='application/json')    

#    # 과거의 영광
#    return jsonify(show_buttons)

# Main
@app.route('/message', methods=['POST'])
def message():
    global contentTO, contentFROM
    dataReceive = request.get_json()
    content = dataReceive['content']

    if u"시작" in content:
        show_buttons = json.dumps({
                                        "message": {
                                        "text": "어디에서 탑승하시나요? 옆으로 쓸어 넘겨 출발지를 찾아보세요."
                                    },
                                        # 버튼은 한 화면에 3개씩 노출
                                        # 최대 10개 노출 가능하다는데 알 방법이 없음
                                        "keyboard": {
                                                        "type": "buttons",
                                                        "buttons": FROM
                                    }
                        })
        return Response(show_buttons, mimetype='application/json')
    elif u"에서" in content:
        contentTO = content
        show_buttons = json.dumps({
                                        "message": {
                                        "text": "어디까지 가시나요? 옆으로 쓸어 넘겨 도착지를 찾아보세요."
                                    },
                                        "keyboard": {
                                                        "type": "buttons",
                                                        "buttons": TO
                                    }
                        })
        return Response(show_buttons, mimetype='application/json')
    elif u"까지" in content:
        contentFROM = content
 
        directionTO = getStationID(contentTO)
        directionFROM = getStationID(contentFROM)
        direction = directionTO - directionFROM
        if direction == 0:
            show_buttons = json.dumps({
                                            "message": {
                                            "text": "출발역과 도착역이 같습니다. 다시 선택해주세요!"
                                        },
                                            "keyboard": {
                                                        "type": "buttons",
                                                        "buttons": FROM
                                        }
                            })
            return Response(show_buttons, mimetype='application/json')
        else:
            print Metro()
            show_buttons = json.dumps({
                                            "message": {
                                            "text": "아직 JSON을 받아오지 못했어요. 처음으로 돌아가세요."
                                        },
                                            "keyboard": {
                                                        "type": "buttons",
                                                        "buttons": RESTART
                                        }
                            })
            return Response(show_buttons, mimetype='application/json')
    elif content == u"사용법":
        show_buttons = json.dumps({
                            "message": {
                                            "text": "도움말인데 아직 내용은..."
                            },
                            "keyboard": {
                                            "type": "buttons",
                                            "buttons": DEFAULT
                            }

                        })
        return Response(show_buttons, mimetype='application/json')
    elif u"처음으로" in content:
        show_buttons = json.dumps({
                            "message": {
                                            "text": "처음 화면입니다. 무엇을 할까요?"
                            },

                            "keyboard": {
                                            "type": "buttons",
                                            "buttons": DEFAULT
                            }
                        })
        return Response(show_buttons, mimetype='application/json')
    elif u"개발사" in content:
        show_buttons = json.dumps({
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
                        })
        return Response(show_buttons, mimetype='application/json')

    else:        
        show_buttons = json.dumps({
                            "message": {
                                            "text": "이해하지 못했어요. 무엇을 할까요?"    
                            },
                            "keyboard": {
                                            "type": "buttons",
                                            "buttons": ["시작하기","사용법","개발사"]
                            }
                        })
        return Response(show_buttons, mimetype='application/json')
#    return jsonify(show_buttons)


if __name__ == '__main__':
    http_server= WSGIServer(('', 3441), app)
    http_server.serve_forever()
