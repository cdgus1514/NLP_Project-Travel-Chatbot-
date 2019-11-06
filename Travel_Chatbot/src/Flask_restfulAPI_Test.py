# -*- coding: utf-8 -*-
from flask import Flask, session, request, g

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
from Users import User_data

###
from datetime import datetime, timedelta
import redis
import _pickle as cPickle
from flask.sessions import SessionInterface, SessionMixin
from werkzeug.datastructures import CallbackDict
from uuid import uuid4
###



## CONFIG
# state = None
check_state_data = dict()
# slot_data = None
check_slot_data = dict()
# pdata = None
check_pdata = dict()
# filename = None
# imgurl = None
# locations = (None, None, None)
check_locations_data = dict()
configs = Configs()
nlp = "nlp"
img = "img"





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
def Trigobot_request():
    global check_slot_data, check_state_data, check_locations_data, check_pdata
    
    # 사용자 데이터 클래스 객체 생성 및 초기화
    _users = session['Userid']
    print('[DEBUG0] check (_users) >> ', _users, end="\n\n")
    _users = User_data()
    if session['Userid'] not in list(check_slot_data.keys()):
        check_slot_data[session['Userid']] = _users.slot_data
    if session['Userid'] not in list(check_state_data.keys()):
        check_state_data[session['Userid']] = _users.state
    if session['Userid'] not in list(check_locations_data.keys()):
        check_locations_data[session['Userid']] = _users.locations
    if session['Userid'] not in list(check_pdata.keys()):
        check_pdata[session['Userid']] = _users.pdata

    print('\n[DEBUG1-0] check_slot_data 확인 >>', check_slot_data, end="\n")
    print('\n[DEBUG1-0] check_state_data 확인 >>', check_state_data, end="\n")
    print('\n[DEBUG1-0] check_locations_data 확인 >>', check_locations_data, end="\n")
    print('\n[DEBUG1-0] check_pdata 확인 >>', check_pdata, end="\n\n")

    print('\n[DEBUG1-0]pdata 메모리 주소 확인 >>', id(_users.pdata), end="\n\n")

    
    if request.method == 'POST':

        ## 유저세션 체크
        c_cookie = request.headers.get('Cookie')
        print("########## session(chatbot) ##########\n", session, end="\n\n")
        # print("[DEBUG1-0] flaskrestful (session.sid) >> ", session.sid, end="\n")
        # print("[DEBUG1-0] flaskrestful (cookie) >> ", c_cookie, end="\n\n\n")
        uid = session['Userid']

        if c_cookie in session.sid:
            print("####### Complete Authentication !!! #######\n\n\n")
        else:
            print("####### Invalid Authentication #######\n\n\n")
            ## 요청 거절 로직

        
        print("\n[DEBUG1-0]flaskrestful (before state) >>", _users.state, end="\n")
        print("\n[DEBUG1-0]flaskrestful (before slot_data) >>", _users.slot_data, end="\n")
        print("\n[DEBUG1-0]flaskrestful (before pdata) >>", _users.pdata, end="\n\n")
        _users.slot_data = check_slot_data[uid]
        _users.state = check_state_data[uid]
        _users.locations = check_locations_data[uid]
        _users.pdata = check_pdata[uid]
        
        # If you requested a slot
        if _users.state is not None and _users.pdata == None:

            data = request.get_json(force=True)
            _users.pdata = data["msg"]

            if _users.state == "restaurant":
                message, _users.state, _users.slot_data, _users.imgurl, _users.locations = restaurant(_users.slot_data, _users.state, _users.pdata, uid)

                print("\n[DEBUG1-3]flask result (after state) >>", _users.state, end="\n")
                print("\n[DEBUG1-3]flask result (after slot_data) >>", _users.slot_data, end="\n")
                print("\n[DEBUG1-3]flask result (after pdata) >>", _users.pdata, end="\n\n\n")

                result = [['message', message], ['sender', 'Trigobot'], ['receiver', data['name']], ['imageurl', _users.imgurl], ['latitude', _users.locations[1]], ['longitude', _users.locations[0]], ['link', _users.locations[2]]]
                result = dict(result)
                check_pdata[uid] = None
                check_slot_data[uid] = None
                check_state_data[uid] = None

                print("\n[DEBUG1-4]flaskrestful - end (state) >>", _users.state, end="\n\n")

                return result
            
            elif _users.state == "weather":
                message, _users.state, _users.slot_data, _users.imgurl, _users.locations = weather(_users.slot_data, _users.state, _users.pdata, uid)
                
                print("\n[DEBUG1-3]flask result (after state) >>", _users.state, end="\n")
                print("\n[DEBUG1-3]flask result (after slot_data) >>", _users.slot_data, end="\n")
                print("\n[DEBUG1-3]flask result (after pdata) >>", _users.pdata, end="\n\n\n")

                result = [['message', message], ['sender', 'Trigobot'], ['receiver', data['name']], ['imageurl', _users.imgurl], ['latitude', _users.locations[1]], ['longitude', _users.locations[0]]]
                result = dict(result)
                check_pdata[uid] = None
                check_slot_data[uid] = None
                check_state_data[uid] = None

                print("\n[DEBUG1-4]flaskrestful - end (state) >>", _users.state, end="\n\n")

                return result

            elif _users.state == "dust":
                message, _users.state, _users.slot_data, _users.imgurl, _users.locations = dust(_users.slot_data, _users.state, _users.pdata, uid)
                
                result = [['message', message], ['sender', 'Trigobot'], ['receiver', data['name']], ['imageurl', _users.imgurl], ['latitude', _users.locations[1]], ['longitude', _users.locations[0]]]
                
                print("\n[DEBUG1-3]flask result (after state) >>", _users.state, end="\n")
                print("\n[DEBUG1-3]flask result (after slot_data) >>", _users.slot_data, end="\n")
                print("\n[DEBUG1-3]flask result (after pdata) >>", _users.pdata, end="\n\n\n")
                
                result = dict(result)
                check_pdata[uid] = None
                check_slot_data[uid] = None
                check_state_data[uid] = None

                print("\n[DEBUG1-4]flaskrestful - end (state) >>", _users.state, end="\n\n")

                return result

            elif _users.state == "travel":
                message, _users.state, _users.slot_data, _users.imgurl, _users.locations = travel(_users.slot_data, _users.state, _users.pdata, uid)
                
                print("\n[DEBUG1-3]flask result (after state) >>", _users.state, end="\n")
                print("\n[DEBUG1-3]flask result (after slot_data) >>", _users.slot_data, end="\n")
                print("\n[DEBUG1-3]flask result (after pdata) >>", _users.pdata, end="\n\n\n")

                result = [['message', message], ['sender', 'Trigobot'], ['receiver', data['name']], ['imageurl', _users.imgurl], ['latitude', _users.locations[1]], ['longitude', _users.locations[0]]]
                result = dict(result)
                check_pdata[uid] = None
                check_slot_data[uid] = None
                check_state_data[uid] = None

                print("\n[DEBUG1-4]flaskrestful (state) >>", _users.state, end="\n\n")

                return result

            elif _users.state == "attraction":
                message, _users.state, _users.slot_data, _users.imgurl, _users.locations = attraction(_users.slot_data, _users.state, _users.pdata, uid)

                print("\n[DEBUG1-3]flask result (after state) >>", _users.state, end="\n")
                print("\n[DEBUG1-3]flask result (after slot_data) >>", _users.slot_data, end="\n")
                print("\n[DEBUG1-3]flask result (after pdata) >>", _users.pdata, end="\n\n\n")

                result = [['message', message], ['sender', 'Trigobot'], ['receiver', data['name']], ['imageurl', _users.imgurl], ['latitude', _users.locations[1]], ['longitude', _users.locations[0]], ['link', _users.locations[2]]]
                result = dict(result)
                check_pdata[uid] = None
                check_slot_data[uid] = None
                check_state_data[uid] = None

                print("\n[DEBUG1-4]flaskrestful - end (state) >>", _users.state, end="\n\n")

                return result
            

        else:
            # Received json data parsing
            data = request.get_json(force=True)
            print("\n[DEBUG1-2]Flaskrestful (req_data) >>", data)
            _users.pdata = data["msg"]

            # Trigobot output
            message, _users.state, _users.slot_data, _users.imgurl, _users.locations = application.run(_users.pdata, _users.state, nlp, uid)
            print("\n[DEBUG1-3]flask result (message) >>", message, end="\n")
            print("\n[DEBUG1-3]flask result (state) >>", _users.state, end="\n")
            print("\n[DEBUG1-3]flask result (slot_data) >>", _users.slot_data, end="\n")
            print("\n[DEBUG1-3]flask result (imgurl) >>", _users.imgurl, end="\n")
            print("\n[DEBUG1-3]flask result (locations) >>", _users.locations, end="\n\n\n")

            # request slot
            if _users.state is not None:
                check_slot_data[uid] = _users.slot_data
                check_state_data[uid] = _users.state
                # check_locations_data[uid] = _users.locations
                print('\n[DEBUG1-0] check_slot_data 확인 >>', check_slot_data, end="\n")
                print('\n[DEBUG1-0] check_state_data 확인 >>', check_state_data, end="\n")
                print('\n[DEBUG1-0] check_locations_data 확인 >>', check_locations_data, end="\n")
                print('\n[DEBUG1-0] check_pdata 확인 >>', check_pdata, end="\n\n")

                result = [['message', message], ['sender', 'Trigobot'], ['receiver', data['name']], ['imageurl', _users.imgurl], ['latitude', _users.locations[1]], ['longitude', _users.locations[0]], ['link', _users.locations[2]]]
                result = dict(result)
                check_pdata[uid] = None

                print("\n[DEBUG 1-4] flaskrestful - end (state) >>", _users.state, end="\n\n")
                
                return result

            # When normal
            else:
                result = [['message', message], ['sender', 'Trigobot'], ['receiver', data['name']], ['imageurl', _users.imgurl], ['latitude', _users.locations[1]], ['longitude', _users.locations[0]], ['link', _users.locations[2]]]
                result = dict(result)
                check_pdata[uid] = None
                check_slot_data[uid] = None
                check_state_data[uid] = None
                
                print("\n[DEBUG 1-4] flaskrestful - end (state) >>", _users.state, end="\n\n")

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
            result = [['message', message], ['sender', 'Trigobot'], ['receiver', 'User'], ['imageurl', None]]
            result = dict(result)
            init = None

            return result



@app.route('/img', methods=['GET', 'POST'])
def img_request():
    global check_pdata
    
    if request.method == 'POST':

        # 사용자 데이터 클래스 객체 생성 및 초기화
        _users = session['Userid']
        print('[DEBUG0] check (_users) >> ', _users, end="\n\n")
        _users = User_data()

        img_file = list(request.files)
        print("\n[DEBUG1-0]img_request (img_file) >>", img_file)

        for file_id in img_file:
            imagefile = request.files[file_id]
            filename = werkzeug.utils.secure_filename(imagefile.filename)
            print("Image Filename : ", imagefile.filename)
            timestr = time.strftime("%Y%m%d-%H%M%S")

            directory = configs.img_path
            filename = directory+timestr+'_'+filename
            imagefile.save(filename)

            print("\n[DEBUG1-1]img_request (filename) >>", filename, end="\n\n")

            message, _users.state, _users.slot_data, _users.imgurl, _users.locations = application.run(filename, _users.state, img, None)
            print("\n[DEBUG1-3]flask result (message) >>", message, end="\n")
            print("\n[DEBUG1-3]flask result (state) >>", _users.state, end="\n")
            print("\n[DEBUG1-3]flask result (slot_data) >>", _users.slot_data, end="\n\n\n")
            print("\n[DEBUG1-3]flask result (imgurl) >>", _users.imgurl, end="\n\n\n")
            print("\n[DEBUG1-3]flask result (locations) >>", _users.locations, end="\n\n\n")

            result = [['message', message], ['sender', 'Trigobot'], ['receiver', 'User'], ['imageurl', _users.imgurl], ['latitude', _users.locations[1]], ['longitude', _users.locations[0]], ['link', _users.locations[2]]]
            result = dict(result)
            _users.filename = None
            
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
            # _users = session['Userid']
            result.insert(0, ['cookie', session.sid])
            print("############# session(login) #############\n", session, end="\n\n")
        else:
            result.insert(0, ['cookie', None])
        
        return dict(result)


if __name__ == "__main__":
    # app.run(host="192.168.0.147", port=30001, threaded=False)
    # app.run(host="192.168.0.147", port=30001)
    app.run(host="192.168.0.147", port=30001, threaded=True)