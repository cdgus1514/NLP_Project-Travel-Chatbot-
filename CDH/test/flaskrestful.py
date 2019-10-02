# -*- coding: utf-8 -*-
from flask import Flask
from flask_restful import Resource, Api, reqparse, request
import application

import json

app = Flask(__name__)
api = Api(app)


class RegistUser(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        # parser.add_argument("name", type=str)
        parser.add_argument("message", type=str)
        args = parser.parse_args()

        # name = args["name"]
        massage = args["message"]
        

        # # 받아온 json 데이터 파싱
        req_data = request.get_json(force=True)
        pdata = req_data["message"]
        # print("pdata >>", pdata)
    
        intent = application.run(pdata)

        result = [['message', intent], ['nickname', 'Chatbot']]
        result = dict(result)

        return result

api.add_resource(RegistUser, '/')



if __name__ == "__main__":
    # app.run(host="192.168.0.154", debug=True)
    app.run(host="192.168.0.147")