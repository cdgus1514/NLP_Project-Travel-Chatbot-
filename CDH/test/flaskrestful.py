# -*- coding: utf-8 -*-
from flask import Flask
from flask_restful import Resource, Api, reqparse, request
import application

from cdh_scenario import restaurant
from cdh_scenario import dust
from cdh_scenario import weather
from cdh_scenario import travel
from cdh_scenario import attraction


import json



app = Flask(__name__)
api = Api(app)

state = None
slot_data = None
pdata = None



class RegistUser(Resource):

    def post(self):

        global state
        global slot_data
        global pdata
        print("\n[DEBUG1-1]flaskrestful (state) >>", state, end="\n\n")

        
        # if you requested a slot
        if state is not None and pdata == None:
            print("\n[DEBUG1-2]flaskrestful (slot_data) >>", slot_data, end="\n\n")
            parser = reqparse.RequestParser()
            parser.add_argument("msg", type=str)
            args = parser.parse_args()

            massage = args["msg"]

            data = request.get_json(force=True)
            pdata = data["msg"]

            if state == "restaurant":
                message, state, slot_data = restaurant(slot_data, state, pdata)
                
                result = [['message', message], ['sender', 'chatbot'], ['receiver', data['name']]]
                result = dict(result)
                # slot_data = None
                pdata = None

                print("\n[DEBUG1-4]flaskrestful (state) >>", state, end="\n\n")

                return result
            
            elif state == "weather":
                message, state, slot_data = weather(slot_data, state, pdata)
                
                result = [['message', message], ['sender', 'chatbot'], ['receiver', data['name']]]
                result = dict(result)
                # slot_data = None
                pdata = None

                print("\n[DEBUG1-4]flaskrestful (state) >>", state, end="\n\n")

                return result

            elif state == "dust":
                message, state, slot_data = dust(slot_data, state, pdata)
                
                result = [['message', message], ['sender', 'chatbot'], ['receiver', data['name']]]
                result = dict(result)
                # slot_data = None
                pdata = None

                print("\n[DEBUG1-4]flaskrestful (state) >>", state, end="\n\n")

                return result

            elif state == "travel":
                message, state, slot_data = travel(slot_data, state, pdata)
                
                result = [['message', message], ['sender', 'chatbot'], ['receiver', data['name']]]
                result = dict(result)
                # slot_data = None
                pdata = None

                print("\n[DEBUG1-4]flaskrestful (state) >>", state, end="\n\n")

                return result

            elif state == "attraction":
                message, state, slot_data = attraction(slot_data, state, pdata)
                
                result = [['message', message], ['sender', 'chatbot'], ['receiver', data['name']]]
                result = dict(result)
                # slot_data = None
                pdata = None

                print("\n[DEBUG1-4]flaskrestful (state) >>", state, end="\n\n")

                return result
        

        else:
            parser = reqparse.RequestParser()
            # parser.add_argument("name", type=str)
            parser.add_argument("msg", type=str)
            args = parser.parse_args()

            # name = args["name"]
            massage = args["msg"]
            
            # # 받아온 json 데이터 파싱
            data = request.get_json(force=True)
            print("\n[DEBUG1-2]Flaskrestful (req_data) >>", data)
            pdata = data["msg"]
            # print("pdata >>", pdata)
            
        
            message, state, slot_data = application.run(pdata, state)
            print("\n[DEBUG1-3]flask result (message) >>", message, end="\n")
            print("\n[DEBUG1-3]flask result (state) >>", state, end="\n")
            print("\n[DEBUG1-3]flask result (slot_data) >>", slot_data, end="\n\n\n")
            

            # request slot
            if state is not None:
                result = [['message', message], ['sender', 'chatbot'], ['receiver', data['name']]]
                result = dict(result)
                pdata = None
                
                return result

            else:
                result = [['message', message], ['sender', 'chatbot'], ['receiver', data['name']]]
                result = dict(result)
                pdata = None
                print("\n[DEBUG 1-4] flaskrestful - end (state) >>", state, end="\n\n")

                return result


api.add_resource(RegistUser, '/')



if __name__ == "__main__":
    app.run(host="192.168.0.147")