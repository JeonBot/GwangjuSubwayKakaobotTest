#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from gevent.wsgi import WSGIServer

app = Flask(__name__)

@app.route('/')
def hello():
    return '안녕하세요?'

@app.route("/keyboard", methods=['GET', 'POST'])
def keyboard():
    #if request.method == 'POST':
    #    print 'POST request'
    #else:
    #    print 'GET request'
    #return u"{'type':'buttons','buttons':['너는 누구니?', '사용법', '지하철']}"
    #return '{"type":"buttons", "buttons":["ch1","ch2","ch3" ]}'
    #return '{"type" : "buttons", "buttons" : ["어디?"]}'
    
    show_buttons = {
                        "type" : "buttons",
                        "buttons" : ["시작하기","도움말"]
                    }
    
    return jsonify(show_buttons)

@app.route("/message", methods=['POST'])
def message():
    dataReceive = request.get_json()
    content = dataReceive['content']

    if content == u"시작하기":
        show_buttons = {
                            "message": {
                                            "text": "안녕하세요?"
                            }
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
                                            "text": "ㅎㅇㅎㅇ"
                            }
                        }
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
