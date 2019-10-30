# -*- coding: utf-8 -*-
from flask import Flask, session, request
# from flask import Session
# from flask_restful import Resource, Api, request

import application

from scenario import restaurant
from scenario import dust
from scenario import weather
from scenario import travel
from scenario import attraction

# from configs import IntentConfigs
from configs import Configs
import json, werkzeug, time
import pymysql as py


###
from datetime import datetime, timedelta
import redis
# import cPickle
import _pickle as cPickle
from flask.sessions import SessionInterface, SessionMixin
from werkzeug.datastructures import CallbackDict
from uuid import uuid4
###


# app = Flask(__name__)
# app.secret_key = 'Handsome boy'
# app.config['SESSION_TYPE'] = 'redis'
# app.session_interface = RedisSessionInterface()
# api = Api(app)

# CONFIG
state = None
slot_data = None
pdata = None
filename = None
imgurl = None
locations = (None, None, None)
nlp = "nlp"
img = "img"

configs = Configs()



####
#########################################################################################
# This is a session object. It is nothing more than a dict with some extra methods
class RedisSession(CallbackDict, SessionMixin):
	def __init__(self, initial=None, sid=None):
		CallbackDict.__init__(self, initial)
		self.sid = sid
		self.modified = False

#########################################################################################
# Session interface is responsible for handling logic related to sessions
# i.e. storing, saving, etc
class RedisSessionInterface(SessionInterface):
	#====================================================================================
	# Init connection
	def __init__(self, host='192.168.0.147', port=6379, db=0, timeout=3600):
		self.store = redis.StrictRedis(host=host, port=port, db=db)
		self.timeout = timeout
	#====================================================================================
	def open_session(self, app, request):
		# Get session id from the cookie
		# sid = request.cookies.get(app.session_cookie_name)
		sid = request.headers.get('Cookie')

		# If id is given (session was created)
		if sid:
			# Try to load a session from Redisdb
			stored_session = None
			ssstr = self.store.get(sid)
			if ssstr:
				stored_session = cPickle.loads(ssstr)
			if stored_session:
				# Check if the session isn't expired
				if stored_session.get('expiration') > datetime.utcnow():
					return RedisSession(initial=stored_session['data'],
										sid=stored_session['sid'])
		
		# If there was no session or it was expired...
		# Generate a random id and create an empty session
		sid = str(uuid4())
		return RedisSession(sid=sid)
	#====================================================================================
	def save_session(self, app, session, response):
		domain = self.get_cookie_domain(app)

		# We're requested to delete the session
		if not session:
			response.delete_cookie(app.session_cookie_name, domain=domain)
			return

		# Refresh the session expiration time
		# First, use get_expiration_time from SessionInterface
		# If it fails, add 1 hour to current time
		if self.get_expiration_time(app, session):
			expiration = self.get_expiration_time(app, session)
		else:
			expiration = datetime.utcnow() + timedelta(hours=1)

		# Update the Redis document, where sid equals to session.sid
		ssd = {
			'sid': session.sid,
			'data': session,
			'expiration': expiration
		}
		ssstr = cPickle.dumps(ssd)
		self.store.setex(session.sid, self.timeout, ssstr)

		# Refresh the cookie
		response.set_cookie(app.session_cookie_name, session.sid,
							expires=self.get_expiration_time(app, session),
							httponly=True, domain=domain)

#########################################################################################










app = Flask(__name__)
app.session_interface = RedisSessionInterface()









# class RegistUser(Resource):
# class Chatbot(Resource):
@app.route('/chatbot', methods=['GET', 'POST'])
# def post(self):
def chatbot_request():
    global state, slot_data, pdata, imgurl, img, locations
    print("\n[DEBUG1-0]flaskrestful (state) >>", state, end="\n\n")

    if request.method == 'POST':
        c_cookie = request.headers.get('cookie')
        print("\n[DEBUG1-0]flask restful (cookie) >> ", c_cookie, end="\n\n")

        print("id check (login) >> ", id(session))
        print("########## session(chatbot) ##########\n", session, end="\n\n")
        if c_cookie in session:
            pass
        else:
            print("Invalid Authentication")

            

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
            # Received json data parsing
            data = request.get_json(force=True)
            print("\n[DEBUG1-2]Flaskrestful (req_data) >>", data)
            pdata = data["msg"]

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



# class HelloUser(Resource):
@app.route('/', methods=['GET', 'POST'])
# def post(self):
def welcome_request():
    if request.method == 'POST':
        # received json data parsing
        data = request.get_json(force=True)
        print("\n[DEBUG1-0]Flaskrestful (req_data) >>", data)
        pdata = data["msg"]
        print("id check (login) >> ", id(session))
        print("########## session(welcom) ##########\n", session, end="\n\n")

        if pdata == "welcom":
            # Welcom msg after first connection
            message = configs.welcome_msg
            result = [['message', message], ['sender', 'chatbot'], ['receiver', 'User'], ['imageurl', None]]
            result = dict(result)
            init = None

            return result



# class ImageAnalysis(Resource):
@app.route('/img', methods=['GET', 'POST'])
# def post(self):
def img_request():
    global img, state, slot_data, imgurl, filename

    if request.method == 'POST':
        img_file = list(request.files)
        print("\n[DEBUG1-0]ImageAnalysis (img_file) >>", img_file)

        for file_id in img_file:
            imagefile = request.files[file_id]
            filename = werkzeug.utils.secure_filename(imagefile.filename)
            print("Image Filename : ", imagefile.filename)
            timestr = time.strftime("%Y%m%d-%H%M%S")

            directory = configs.img_path
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



# class Login(Resource):
@app.route('/login', methods=['GET', 'POST'])
# def post(self):
def login():
    if request.method == 'POST':
        data = request.get_json(force=True)
        print("\n[DEBUG1-0]Flaskrestful (req_data) >>", data, end="\n\n\n")

        Userid = data["id"]
        Userpw = data["password"]

        print("\n\nInput >> ", Userid, Userpw, end="\n\n")
        ## 데이터베이스에서 id/pw 체크 >> 맞으면 True, 틀리면 Flase
        conn = py.connect(host="cdgus1514.cafe24.com", user="cdgus1514", password="Chlehd131312", database="cdgus1514", charset="utf8")
        cursor = conn.cursor()
        
        query = "SELECT user_id, user_pw FROM chatbot_users WHERE user_id = %s"
        value = (Userid)
        cursor.execute("set names utf8")
        cursor.execute(query, value)
        check_user = cursor.fetchone()

        cursor.close()
        conn.close()

        try:
            print(check_user, end="\n\n")   #튜플
            # print("ID >> ", check_user[0][0])
            # print("PW >> ", check_user[0][1], end="\n\n")
            print("ID >> ", check_user[0])
            print("PW >> ", check_user[1], end="\n\n\n")

        except:
            # session.pop('Userid')
            print("############# session(login) #############\n", session, end="\n\n\n")
            message = "############## Failed Login ##############\n\n\n\n"
            print(message)

            result = [['cookie', Userid], ['nick', Userid], ['state', None]]


            return dict(result)


        # ID/PW 체크
        if Userid == check_user[0] and Userpw == check_user[1]:
            
            # Session
            session['Userid'] = Userid
            # session['Userid'] = request.args.get('id')
            print("id check (login) >> ", id(session))
            print("############# session(login) #############\n", session, end="\n\n")

            message = "############## Success Login!!! ##############\n\n\n\n"
            print(message)

            result = [['cookie', session.sid], ['nick', Userid], ['state', 'OK']]
            session
            return dict(result)
        
        else:
            print("############# session(login) #############\n", session, end="\n\n\n")

            message = "############## Failed Login ##############\n\n\n\n"
            print(message)

            result = [['cookie', Userid], ['nick', Userid], ['state', None]]

            return dict(result)



# api.add_resource(Login, '/login')
# api.add_resource(HelloUser, '/')
# api.add_resource(Chatbot, '/chatbot')
# api.add_resource(ImageAnalysis, '/img')



if __name__ == "__main__":
    # app.run(host="192.168.0.147", port=30001, threaded=False)
    app.run(host="192.168.0.147", port=30001)