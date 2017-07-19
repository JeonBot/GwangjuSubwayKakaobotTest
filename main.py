# !/usr/bin/env python
# -*- coding: utf-8 -*-

# For data load
import urllib, json, datetime, requests, random, time, threading, sys

from flask import Flask, request, jsonify, Response, send_from_directory
from gevent.wsgi import WSGIServer

app = Flask(__name__)

# For default encoding to utf-8 instead ascii
reload(sys)
sys.setdefaultencoding('utf-8')

# Static list
FROM = ["녹동에서","소태에서","학동증심사입구에서","남광주에서","문화전당에서","금남로4가에서","금남로5가에서","양동시장에서","돌고개에서","농성에서","화정에서","운천에서","상무에서","쌍촌에서","김대중컨벤션센터에서","공항에서","송정공원에서","광주송정에서","도산에서","평동에서"]
TO = ["녹동까지","소태까지","학동증심사입구까지","남광주까지","문화전당까지","금남로4가까지","금남로5가까지","양동시장까지","돌고개까지","농성까지","화정까지","운천까지","상무까지","쌍촌까지","김대중컨벤션센터까지","공항까지","송정공원까지","광주송정까지","도산까지","평동까지"]
DEFAULT = ["시작하기","사용법","개발사"]
STATIONDIC = {u'녹동에서': 100, u'녹동까지':100, u'소태에서': 101, u'소태까지':101, u'학동증심사입구에서': 102, u'학동증심사입구까지':102, u'남광주에서': 103, u'남광주까지':103, u'문화전당에서': 104, u'문화전당까지':104, u'금남로4가에서': 105, u'금남로4가까지':105, u'금남로5가에서': 106, u'금남로5가까지':106, u'양동시장에서': 107, u'양동시장까지':107, u'돌고개에서': 108, u'돌고개까지':108, u'농성에서': 109, u'농성까지':109, u'화정에서': 110, u'화정까지':110, u'운천에서': 111, u'운천까지':111, u'상무에서': 112, u'상무까지':112, u'쌍촌에서': 113, u'쌍촌까지':113, u'김대중컨벤션센터에서': 114, u'김대중컨벤션센터까지':114, u'공항에서': 115, u'공항까지':115, u'송정공원에서': 116, u'송정공원까지':116, u'광주송정에서': 117, u'광주송정까지':117, u'도산에서': 118, u'도산까지':118, u'평동에서': 119, u'평동까지':119}
STATIONDICTOSTR = {100: u'녹동', 101: u'소태', 102: u'학동증심사입구', 103: u'남광주', 104: u'문화전당', 105: u'금남로4가', 106: u'금남로5가', 107: u'양동시장', 108: u'돌고개', 109: u'농성', 110: u'화정', 111: u'운천', 112: u'상무', 113: u'쌍촌', 114: u'김대중컨벤션센터', 115: u'공항', 116: u'송정공원', 117: u'광주송정', 118: u'도산', 119: u'평동',} 
RESTART = ["처음으로", "열차검색다시시작"]

# StationName to Integer
def getStationID(stationName):
    try:
        stationIDdict = STATIONDIC[stationName]
        return stationIDdict
    except:
        print "Exception non existing Station Name: ", stationName
        return None

# Integer to StationName
def getIntegerID(stationNum):
    try:
        stationIDdicttoSTR = STATIONDICTOSTR[stationNum]
        return stationIDdicttoSTR
    except:
        print "Exception non existing Station Name: ", stationNum
        return None

# Metro Information
def Metro():
    # Changeable port number
    url = 'http://energy.openlab.kr:3003'
    
    # Load and Save data
    u = urllib.urlopen(url)
    data = u.read()
    j = json.loads(data)    
    subway = j["subway"]

    # Total subway
    i = 0

    # Array call
    subinfo = []
    traininfo = []
    trainloc = []
    traindir = []
    humavg = []
    tempavg = []
    
    # initialization
    for l in range(0,10):
        subinfo.append(l)
        traininfo.append(l)
        trainloc.append(l)
        traindir.append(l)
        humavg.append(l)
        tempavg.append(l)
    
    # JSON call and Threading
    try:
        for i in range(0,10):
            if subway[i] != None:
                subinfo = subway[i]
                traininfo[i] = subinfo["Train"]
                trainloc[i] = subinfo["Location"]
                traindir[i] = subinfo["work"]
                humavg[i] = (subinfo["T1HUM"] + subinfo["T2HUM"] + subinfo["T3HUM"] + subinfo["T4HUM"]) / 4
                tempavg[i] = (subinfo["T1TEMP"] + subinfo["T2TEMP"] + subinfo["T3TEMP"] + subinfo["T4TEMP"]) / 4
    except (ValueError, IndexError) as e:
        pass
    try:
        threading.Timer(10,Metro).start()
#        # time.sleep을 걸지 않으면 try-except를 거치지 않는다는데
#        # 막상 걸면 sys.exit()가 수행이 안되고 interrupt를 줘도 무응답으로 일관함
#        # 어떤 interrupt를 줘도 무응답이어서 연결 자체를 종료하고 재접속해야함
#        # 어떻게 해결하면 좋을까?
#        while True: time.sleep(100)
    except (KeyboardInterrupt, SystemExit):
        print '\n! Received keyboard interrupt, quitting threads.\n'
    return (traininfo, trainloc, traindir, humavg, tempavg, i)

#@app.route('/')
#def hello():
#    return "안녕하세요?"

@app.route('/keyboard', methods=['GET'])
def keyboard():
    show_buttons = json.dumps({
                                "type": "buttons",
                                "buttons": DEFAULT
                    })
    return Response(show_buttons, mimetype='application/json')


#    # 바로 시작
#    # content = request.get_json()    
#    show_buttons = json.dumps({
#                    # 버튼은 한 화면에 3개씩 노출
#                    # 최대 10개 노출 가능하다는데 알 방법이 없음
#                                "type": "buttons",
#                                "buttons": TO
#                    })
#    return Response(show_buttons, mimetype='application/json')


#    # 첫 화면을 아무말로.
#    response = json.dumps({"type" : "text"})
#    return Response(response, mimetype='application/json')    

#    # 과거의 영광
#    return jsonify(show_buttons)


# Main
@app.route('/message', methods=['POST'])
def message():
    # Global variable for direction
    global contentTO, contentFROM
    
    # Load of user's selected button
    dataReceive = request.get_json()
    content = dataReceive['content']

    if u"시작" in content:
        show_buttons = json.dumps({
                                        "message": {
                                        "text": "어디에서 출발하시나요? 옆으로 쓸어 넘겨 출발지를 찾아보세요."
                                    },
                                        # 버튼은 한 화면에 3개씩 노출
                                        # 최대 10개 노출 가능하다는데 어떻게하지?
                                        "keyboard": {
                                                        "type": "buttons",
                                                        "buttons": FROM
                                    }
                        })
        return Response(show_buttons, mimetype='application/json')
    elif u"에서" in content:
        # user's selected departure
        contentFROM = content
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
        # user's selected destination        
        contentTO = content
 
        # transform to integer
        directionFROM = getStationID(contentFROM)
        directionTO = getStationID(contentTO)
        direction = directionFROM - directionTO
        
        # When someone is click same buttons
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
        # direction != 0
        else:
            # To total
            i = 0
            # Metro array call and Metro return values load
            subinformation = []
            subinformation = Metro()
    
            # Array call
            traininfo = []
            trainloc = []
            traindir = []
            humavg = []
            tempavg = []
            text_arr = []
                        
            # List save
            traininfo = subinformation[0]
            trainloc = subinformation[1]
            traindir = subinformation[2]
            humavg = subinformation[3]
            tempavg = subinformation[4]
            total = subinformation[5]

            # initialization            
            for l in range(0,total):
                text_arr.append(l)
 
            # Output information string part of part
            text0 = "상행 : 녹동(소태) → 평동\n하행 : 평동 → 녹동(소태)\n"
            text1 = "운행 중인 열차는 %d대 입니다.\n――――――――\n" % (total)
            text2 = ""
            
            # JSON load and final String maker
            for i in range(total):
                # Integer station to string station
                all_train_pos = getIntegerID(trainloc[i])
                
                # Output station information string part of part
                text2_1 = str(all_train_pos)
                
                # Load hum and temp data
                all_train_humavg = humavg[i]
                all_train_tempavg = tempavg[i]
                
                # Lead time
                minute = abs((directionFROM - trainloc[i]) * 2)
                
                # Probability for boarding
                # Pass by or not
                if directionFROM < trainloc[i] and traindir[i] == 0:
                    text2_2 = "역에 있는 상행 열차는 약 %d분 전에 이 역을 지나갔습니다.\n평균 온도 : %d℃ , 평균 습도 : %d%%\n――――――――\n" % (minute, all_train_tempavg, all_train_humavg)
                    text_arr[i] = text2_1 + text2_2
                    text2 = text2 + text_arr[i]
                elif directionFROM > trainloc[i] and traindir[i] == 0:
                    text2_2 = "역에 있는 상행 열차는 약 %d분 후에 이 역에 도착합니다.\n평균 온도 : %d℃ , 평균 습도 : %d%%\n――――――――\n" % (minute, all_train_tempavg, all_train_humavg)
                    text_arr[i] = text2_1 + text2_2
                    text2 = text2 + text_arr[i]
                elif directionFROM < trainloc[i] and traindir[i] == 1:
                    text2_2 = "역에 있는 하행 열차는 약 %d분 후에 이 역에 도착합니다.\n평균 온도 : %d℃ , 평균 습도 : %d%%\n――――――――\n" % (minute, all_train_tempavg, all_train_humavg)
                    text_arr[i] = text2_1 + text2_2
                    text2 = text2 + text_arr[i]
                elif directionFROM > trainloc[i] and traindir[i] == 1:
                    text2_2 = "역에 있는 하행 열차는 약 %d분 전에 이 역을 지나갔습니다.\n평균 온도 : %d℃ , 평균 습도 : %d%%\n――――――――\n" % (minute, all_train_tempavg, all_train_humavg)
                    text_arr[i] = text2_1 + text2_2
                    text2 = text2 + text_arr[i]
                elif directionFROM == trainloc[i]:
                    text2 = "열차가 곧 도착하거나 지나갔습니다.\n――――――――\n"
            
            # Complete output string
                text = text0 + text1 + text2
    
                show_buttons = json.dumps({
                                                "message": {
                                                "text": text
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

#    # 과거의 영광2
#    return jsonify(show_buttons)

if __name__ == '__main__':
    http_server= WSGIServer(('', 3441), app)
    http_server.serve_forever()
