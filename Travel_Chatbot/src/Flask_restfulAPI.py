# -*- coding: utf-8 -*-
from flask import Flask, session, request

import application

from scenario import restaurant
from scenario import dust
from scenario import weather
from scenario import travel
from scenario import attraction

from configs import Configs
import json, werkzeug, time

from util.logindb import checkUser
# from util.signupdb import addUser


###
from datetime import datetime, timedelta
import redis
import _pickle as cPickle
from flask.sessions import SessionInterface, SessionMixin
from werkzeug.datastructures import CallbackDict
from uuid import uuid4
###



## CONFIG
state = None
slot_data = None
pdata = None
filename = None
imgurl = None
locations = (None, None, None)
nlp = "nlp"
img = "img"

configs = Configs()



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



@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot_request():
    global state, slot_data, pdata, imgurl, img, locations
    print("\n[DEBUG1-0]flaskrestful (state) >>", state, end="\n\n")

    if request.method == 'POST':
        ## Check Cookie & session.sid
        c_cookie = request.headers.get('Cookie')
        print("########## session(chatbot) ##########\n", session, end="\n\n")
        # print("[DEBUG1-0] flaskrestful (session.sid) >> ", session.sid, end="\n")
        # print("[DEBUG1-0] flaskrestful (cookie) >> ", c_cookie, end="\n\n\n")
        uid = session['Userid']

        if c_cookie in session.sid:
            print("####### Complete Authentication !!! #######\n\n\n")
            pass
        else:
            print("####### Invalid Authentication #######\n\n\n")
            ## 요청 거절
            # result = [['message', message], ['sender', 'chatbot'], ['receiver', data['name']], ['imageurl', imgurl], ['latitude', locations[1]], ['longitude', locations[0]], ['link', locations[2]]]
            # result = dict(result)
            
            # return result

            
        # If you requested a slot
        if state is not None and pdata == None:
            print("\n[DEBUG1-2]flaskrestful (slot_data) >>", slot_data, end="\n\n")

            data = request.get_json(force=True)
            pdata = data["msg"]

            if state == "restaurant":
                message, state, slot_data, imgurl, locations = restaurant(slot_data, state, pdata, uid)
                
                result = [['message', message], ['sender', 'chatbot'], ['receiver', data['name']], ['imageurl', imgurl], ['latitude', locations[1]], ['longitude', locations[0]], ['link', locations[2]]]
                result = dict(result)
                pdata = None

                print("\n[DEBUG1-4]flaskrestful (state) >>", state, end="\n\n")

                return result
            
            elif state == "weather":
                message, state, slot_data, imgurl, locations = weather(slot_data, state, pdata, uid)
                
                result = [['message', message], ['sender', 'chatbot'], ['receiver', data['name']], ['imageurl', imgurl], ['latitude', locations[1]], ['longitude', locations[0]]]
                result = dict(result)
                pdata = None

                print("\n[DEBUG1-4]flaskrestful (state) >>", state, end="\n\n")

                return result

            elif state == "dust":
                message, state, slot_data, imgurl, locations = dust(slot_data, state, pdata, uid)
                
                result = [['message', message], ['sender', 'chatbot'], ['receiver', data['name']], ['imageurl', imgurl], ['latitude', locations[1]], ['longitude', locations[0]]]
                result = dict(result)
                pdata = None

                print("\n[DEBUG1-4]flaskrestful (state) >>", state, end="\n\n")

                return result

            elif state == "travel":
                message, state, slot_data, imgurl, locations = travel(slot_data, state, pdata, uid)
                
                result = [['message', message], ['sender', 'chatbot'], ['receiver', data['name']], ['imageurl', imgurl], ['latitude', locations[1]], ['longitude', locations[0]]]
                result = dict(result)
                pdata = None

                print("\n[DEBUG1-4]flaskrestful (state) >>", state, end="\n\n")

                return result

            elif state == "attraction":
                message, state, slot_data, imgurl, locations = attraction(slot_data, state, pdata, uid)

                result = [['message', message], ['sender', 'chatbot'], ['receiver', data['name']], ['imageurl', imgurl], ['latitude', locations[1]], ['longitude', locations[0]], ['link', locations[2]]]
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
            message, state, slot_data, imgurl, locations = application.run(pdata, state, nlp, uid)
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



@app.route('/', methods=['GET', 'POST'])
def welcome_request():
    if request.method == 'POST':
        # received json data parsing
        data = request.get_json(force=True)
        print("\n[DEBUG1-0]Flaskrestful (req_data) >>", data)
        pdata = data["msg"]

        print("########## session(welcom) ##########\n", session, end="\n\n")
        if pdata == "welcom":
            # Welcom msg after first connection
            message = configs.welcome_msg
            result = [['message', message], ['sender', 'chatbot'], ['receiver', 'User'], ['imageurl', None]]
            result = dict(result)
            init = None

            return result



@app.route('/img', methods=['GET', 'POST'])
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

            message, state, slot_data, imgurl, locations = application.run(filename, state, img, None)
            print("\n[DEBUG1-3]flask result (message) >>", message, end="\n")
            print("\n[DEBUG1-3]flask result (state) >>", state, end="\n")
            print("\n[DEBUG1-3]flask result (slot_data) >>", slot_data, end="\n\n\n")
            print("\n[DEBUG1-3]flask result (imgurl) >>", imgurl, end="\n\n\n")
            print("\n[DEBUG1-3]flask result (locations) >>", locations, end="\n\n\n")

            result = [['message', message], ['sender', 'chatbot'], ['receiver', 'User'], ['imageurl', imgurl], ['latitude', locations[1]], ['longitude', locations[0]], ['link', locations[2]]]
            result = dict(result)
            filename = None
            
            return result



@app.route('/login', methods=['GET', 'POST'])
def login_request():
    if request.method == 'POST':
        data = request.get_json(force=True)
        print("\n[DEBUG1-0]Flaskrestful (req_data) >>", data, end="\n\n\n")

        Userid = data["id"]
        Userpw = data["password"]

        result, check =  checkUser(Userid, Userpw)

        # Create Cookie & Session
        if check == True:
            session['Userid'] = Userid
            result.insert(0, ['cookie', session.sid])
            print("############# session(login) #############\n", session, end="\n\n")
        else:
            result.insert(0, ['cookie', None])
        
        return dict(result)



if __name__ == "__main__":
    # app.run(host="192.168.0.147", port=30001, threaded=False)
    # app.run(host="192.168.0.147", port=30001)
    app.run(host="192.168.0.147", port=30001, threaded=True)