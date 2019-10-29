# -*- coding: utf-8 -*-
from flask import Flask
from flask_restful import Resource, Api, request

import application

from scenario import restaurant
from scenario import dust
from scenario import weather
from scenario import travel
from scenario import attraction

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
locations = (None, None, None)
nlp = "nlp"
img = "img"
config = Configs()



class RegistUser(Resource):
    def post(self):
        global state, slot_data, pdata, imgurl, img, locations
        print("\n[DEBUG1-0]flaskrestful (state) >>", state, end="\n\n")


        # If you requested a slot
        if state is not None and pdata == None:
            print("\n[DEBUG1-2]flaskrestful (slot_data) >>", slot_data, end="\n\n")

            data = request.get_json(force=True)
            pdata = data["msg"]

            if state == "restaurant":
                message, state, slot_data, imgurl, locations = restaurant(slot_data, state, pdata)
                
                result = [['message', message], ['sender', 'chatbot'], ['receiver', data['name']], ['imageurl', imgurl], ['latitude', locations[0]], ['longitude', locations[1]]]
                result = dict(result)
                pdata = None

                print("\n[DEBUG1-4]flaskrestful (state) >>", state, end="\n\n")

                return result
            
            elif state == "weather":
                message, state, slot_data, imgurl, locations = weather(slot_data, state, pdata)
                
                result = [['message', message], ['sender', 'chatbot'], ['receiver', data['name']], ['imageurl', imgurl], ['latitude', locations[0]], ['longitude', locations[1]]]
                result = dict(result)
                pdata = None

                print("\n[DEBUG1-4]flaskrestful (state) >>", state, end="\n\n")

                return result

            elif state == "dust":
                message, state, slot_data, imgurl, locations = dust(slot_data, state, pdata)
                
                result = [['message', message], ['sender', 'chatbot'], ['receiver', data['name']], ['imageurl', imgurl], ['latitude', locations[0]], ['longitude', locations[1]]]
                result = dict(result)
                pdata = None

                print("\n[DEBUG1-4]flaskrestful (state) >>", state, end="\n\n")

                return result

            elif state == "travel":
                message, state, slot_data, imgurl, locations = travel(slot_data, state, pdata)
                
                result = [['message', message], ['sender', 'chatbot'], ['receiver', data['name']], ['imageurl', imgurl], ['latitude', locations[0]], ['longitude', locations[1]]]
                result = dict(result)
                pdata = None

                print("\n[DEBUG1-4]flaskrestful (state) >>", state, end="\n\n")

                return result

            elif state == "attraction":
                message, state, slot_data, imgurl, locations = attraction(slot_data, state, pdata)

                result = [['message', message], ['sender', 'chatbot'], ['receiver', data['name']], ['imageurl', imgurl], ['latitude', locations[0]], ['longitude', locations[1]]]
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
            message, state, slot_data, imgurl, locations = application.run(pdata, state, nlp)
            print("\n[DEBUG1-3]flask result (message) >>", message, end="\n")
            print("\n[DEBUG1-3]flask result (state) >>", state, end="\n")
            print("\n[DEBUG1-3]flask result (slot_data) >>", slot_data, end="\n\n\n")
            print("\n[DEBUG1-3]flask result (imgurl) >>", imgurl, end="\n\n\n")
            print("\n[DEBUG1-3]flask result (locations) >>", locations, end="\n\n\n")

            # request slot
            if state is not None:
                result = [['message', message], ['sender', 'chatbot'], ['receiver', data['name']], ['imageurl', imgurl], ['latitude', locations[1]], ['longitude', locations[0]], ['link', locations[2]]]
                result = dict(result)
                pdata = None
                
                return result

            # When normal
            else:
                result = [['message', message], ['sender', 'chatbot'], ['receiver', data['name']], ['imageurl', imgurl], ['latitude', locations[1]], ['longitude', locations[0]], ['link', locations[2]]]

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
            result = [['message', message], ['sender', 'chatbot'], ['receiver', 'User'], ['imageurl', None]]
            result = dict(result)
            init = None

            return result



class ImageAnalysis(Resource):
    def post(self):
        global img, state, slot_data, imgurl, filename

        img_file = list(request.files)
        print("\n[DEBUG1-0]ImageAnalysis (img_file) >>", img_file)

        for file_id in img_file:
            imagefile = request.files[file_id]
            filename = werkzeug.utils.secure_filename(imagefile.filename)
            print("Image Filename : ", imagefile.filename)
            timestr = time.strftime("%Y%m%d-%H%M%S")

            directory = config.img_path
            filename = directory+timestr+'_'+filename
            imagefile.save(filename)

            print("\n[DEBUG1-1]ImageAnalysis (filename) >>", filename, end="\n\n")

            message, state, slot_data, imgurl, locations = application.run(filename, state, img)
            print("\n[DEBUG1-3]flask result (message) >>", message, end="\n")
            print("\n[DEBUG1-3]flask result (state) >>", state, end="\n")
            print("\n[DEBUG1-3]flask result (slot_data) >>", slot_data, end="\n\n\n")
            print("\n[DEBUG1-3]flask result (imgurl) >>", imgurl, end="\n\n\n")
            print("\n[DEBUG1-3]flask result (locations) >>", locations, end="\n\n\n")

            result = [['message', message], ['sender', 'chatbot'], ['receiver', 'User'], ['imageurl', imgurl], ['latitude', locations[1]], ['longitude', locations[0]], ['link', locations[2]]]
            result = dict(result)
            filename = None
            
            return result



api.add_resource(HelloUser, '/')
api.add_resource(RegistUser, '/chatbot')
api.add_resource(ImageAnalysis, '/img')



if __name__ == "__main__":
    app.run(host="192.168.0.147", port=30001)