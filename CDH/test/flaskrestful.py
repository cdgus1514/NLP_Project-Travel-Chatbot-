# -*- coding: utf-8 -*-
from flask import Flask
from flask_restful import Resource, Api, reqparse, request

import application

from cdh_scenario import restaurant
from cdh_scenario import dust
from cdh_scenario import weather
from cdh_scenario import travel
from cdh_scenario import attraction

# from configs import IntentConfigs
from configs import Configs

import json, werkzeug, time



app = Flask(__name__)
api = Api(app)

# CONFIG
state = None
slot_data = None
pdata = None
filename = None
imgurl = None
nlp = "nlp"
img = "img"
# config = IntentConfigs()
config = Configs()



class RegistUser(Resource):

    def post(self):

        global state
        global slot_data
        global pdata
        global imgurl
        global img
        print("\n[DEBUG1-0]flaskrestful (state) >>", state, end="\n\n")


        # if you requested a slot
        if state is not None and pdata == None:
            print("\n[DEBUG1-2]flaskrestful (slot_data) >>", slot_data, end="\n\n")

            data = request.get_json(force=True)
            pdata = data["msg"]

            if state == "restaurant":
                message, state, slot_data, imgurl = restaurant(slot_data, state, pdata)
                
                result = [['message', message], ['sender', 'chatbot'], ['receiver', data['name']]]
                result = dict(result)
                pdata = None

                print("\n[DEBUG1-4]flaskrestful (state) >>", state, end="\n\n")

                return result
            
            elif state == "weather":
                message, state, slot_data, imgurl = weather(slot_data, state, pdata)
                
                result = [['message', message], ['sender', 'chatbot'], ['receiver', data['name']]]
                result = dict(result)
                pdata = None

                print("\n[DEBUG1-4]flaskrestful (state) >>", state, end="\n\n")

                return result

            elif state == "dust":
                message, state, slot_data, imgurl = dust(slot_data, state, pdata)
                
                result = [['message', message], ['sender', 'chatbot'], ['receiver', data['name']]]
                result = dict(result)
                pdata = None

                print("\n[DEBUG1-4]flaskrestful (state) >>", state, end="\n\n")

                return result

            elif state == "travel":
                message, state, slot_data, imgurl = travel(slot_data, state, pdata)
                
                result = [['message', message], ['sender', 'chatbot'], ['receiver', data['name']]]
                result = dict(result)
                pdata = None

                print("\n[DEBUG1-4]flaskrestful (state) >>", state, end="\n\n")

                return result

            elif state == "attraction":
                message, state, slot_data, imgurl = attraction(slot_data, state, pdata)
                
                result = [['message', message], ['sender', 'chatbot'], ['receiver', data['name']]]
                result = dict(result)
                pdata = None

                print("\n[DEBUG1-4]flaskrestful (state) >>", state, end="\n\n")

                return result
        

        else:            
            # received json data parsing
            data = request.get_json(force=True)
            print("\n[DEBUG1-2]Flaskrestful (req_data) >>", data)
            pdata = data["msg"]
            # print("pdata >>", pdata)

            # Chatbot output
            message, state, slot_data, imgurl = application.run(pdata, state, nlp)
            print("\n[DEBUG1-3]flask result (message) >>", message, end="\n")
            print("\n[DEBUG1-3]flask result (state) >>", state, end="\n")
            print("\n[DEBUG1-3]flask result (slot_data) >>", slot_data, end="\n\n\n")
            print("\n[DEBUG1-3]flask result (imgurl) >>", imgurl, end="\n\n\n")
            

            # request slot
            if state is not None:
                result = [['message', message], ['sender', 'chatbot'], ['receiver', data['name']]]
                result = dict(result)
                pdata = None
                
                return result

            # When normal
            else:
                result = [['message', message], ['sender', 'chatbot'], ['receiver', data['name']]]
                result = dict(result)
                pdata = None
                print("\n[DEBUG 1-4] flaskrestful - end (state) >>", state, end="\n\n")

                return result



class HelloUser(Resource):

    def post(self):        
        # received json data parsing
        data = request.get_json(force=True)
        print("\n[DEBUG1-2]Flaskrestful (req_data) >>", data)
        pdata = data["msg"]

        if pdata == "welcom":
            # Welcom msg after first connection
            message = config.welcome_msg
            result = [['message', message], ['sender', 'chatbot'], ['receiver', 'User']]
            result = dict(result)
            init = None

            return result



class ImageAnalysis(Resource):

    def post(self):
        global img
        global state
        global slot_data
        global imgurl
        global filename

        img_file = list(request.files)
        print("\n[DEBUG1-0]ImageAnalysis (img_file) >>", img_file)

        for file_id in img_file:
            imagefile = request.files[file_id]
            # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", imagefile)
            filename = werkzeug.utils.secure_filename(imagefile.filename)
            print("Image Filename : ", imagefile.filename)
            timestr = time.strftime("%Y%m%d-%H%M%S")

            directory = config.img_path
            filename = directory+timestr+'_'+filename
            imagefile.save(filename)

            print("\n[DEBUG1-1]ImageAnalysis (filename) >>", filename, end="\n\n")

            message, state, slot_data, imgurl = application.run(filename, state, img)
            print("\n[DEBUG1-3]flask result (message) >>", message, end="\n")
            print("\n[DEBUG1-3]flask result (state) >>", state, end="\n")
            print("\n[DEBUG1-3]flask result (slot_data) >>", slot_data, end="\n\n\n")
            print("\n[DEBUG1-3]flask result (imgurl) >>", imgurl, end="\n\n\n")


            result = [['message', message], ['sender', 'chatbot'], ['receiver', 'User']]
            result = dict(result)
            filename = None
            
            return result



api.add_resource(HelloUser, '/')
api.add_resource(RegistUser, '/chatbot')
api.add_resource(ImageAnalysis, '/img')



if __name__ == "__main__":
    app.run(host="192.168.0.147", port=30001)