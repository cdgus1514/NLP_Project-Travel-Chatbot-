# -*- coding: utf-8 -*-
from flask import Flask
from flask_restful import Resource, Api, reqparse, request
import application

import json

app = Flask(__name__)
api = Api(app)

class RegistUser(Resource):
    def post(self):
        state = None
        parser = reqparse.RequestParser()
        # parser.add_argument("name", type=str)
        parser.add_argument("msg", type=str)
        args = parser.parse_args()

        # name = args["name"]
        massage = args["msg"]
        

        # # 받아온 json 데이터 파싱
        data = request.get_json(force=True)
        print("\n[DEBUG1-1]Flaskrestful (req_data) >>", data)
        pdata = data["msg"]
        # print("pdata >>", pdata)
    
        message = application.run(pdata)

        result = [['message', message], ['sender', 'chatbot'], ['receiver', data['name']]]
        result = dict(result)
        # print("\n[DEBUG1-2]Flaskrestful (result) >>", result)
        print("\n\n[DEBUG]flaskrestful (state) >>", state)

        return result

api.add_resource(RegistUser, '/')



if __name__ == "__main__":
    app.run(host="192.168.0.147")