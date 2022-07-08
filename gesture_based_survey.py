#!/usr/bin/env python3
#
#
# Prerequisites:
# ---------------
# - jetpack 4.0
# - pip install flask
# - pip install numpy
# - pip install opencv-contrib-python
# - pip install imutils
# - pip install tensorty  
# Note:
# -----
# MULTI_THREAD_EN env can be applied for enabling/disabling multi-thread setup, i.e. whether or not video processing
# will be done in a separate thread or not (might become sensitive when running in a production server).
#
# 
# ---------------------------------------------------------------------------------------------------


from flask import Response, Flask, render_template, session, request, jsonify,stream_with_context
from flask_session import Session
import cv2
import model_process
import socket
#import threading
import argparse
import datetime
import time
import string
import random
import os
import threading
import json
#import numpy as np
import pandas as pd
import traceback
import logging
import requests
from requests.exceptions import HTTPError, ConnectTimeout, ReadTimeout
from typing import Tuple
import io
import webbrowser
#import GenerateQrCode
import platform
from urllib import request as reqs

# ---------------------------------------------------------------------------------------------------
# Globals:

"""
#Log capture -- Subham
logging.basicConfig(filename="./logs/{}.log".format(dt.datetime.today().date()),level=logging.DEBUG,format='%(asctime)s %(levelname)s: %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
"""
# JSON parameter input : {'device': '192.168.0.11', 'port': '8081', 'camera':'CSI','cameraip':'192.168.0.3','camuser':'admin','campass':'admin','multithreded':'Y'}

with open('parameter.json') as f:
  paramval = json.load(f)

uri = 'http://admin:admin@127.0.0.1:8081/video'
frame=None
buffer=None
transform = None
lst = []
ln=1
gesans = 'None'
qmode="Gesture"  
key = 0
working_start_time = time.time()
df=pd.DataFrame()
lfile=None
oimap={}


remote_ip = os.environ.get('REMOTE_IP', uri)
local_mode = (remote_ip == paramval['device']) ##"192.168.0.16")

sess=None

futures = dict()
 
hostname =socket.gethostname() 
ipaddress=socket.gethostbyname("")

""" Generate Serial Number """
def getSerialNumber():
	os_type = platform.system()
	print(os_type)
	
	if "Windows" in os_type:
		command = "wmic bios get serialnumber"
		retstr= os.popen(command).read().strip().split("\n")[2]

	if "Linux" in os_type:
		command = "sudo dmidecode -t system"
		try:
			retstr= os.popen(command).read().strip().split("\n")[9]	
			retstr=retstr.strip().split(":")[1]
		except:
			print("##### GET SERIAL NUMBER NOT WORKING #####")
			retstr = "ERROR"

	return retstr

hostsrl = getSerialNumber()


gcpdata={}

def get_callback(f, data):
    def callback(f):
        try:
            # print(f.result())
            futures.pop(data)
        except:
            print("Please handle {} for {}.".format(f.exception(), data))
 
    return callback


# ---------------------------------------------------------------------------------------------------
# Initialize a flask object
app = Flask(__name__)
app.secret_key='peter'
# ---------------------------------------------------------------------------------------------------
# Initialize the video stream and allow the camera sensor to warmup
camurl='http://'+paramval['cameraip']+':'+paramval['cameraport']+'@'+paramval['camerauser']+':'+paramval['camerapwd']+'/'+paramval['cameraurl']
print(camurl)

if paramval['camera'] == '' or paramval['camerastream'] == '' :
	print('Choose Camera and stream ')
	exit()
else :
	if paramval['camerastream'] == 'http':
		if paramval['camera'].upper() == 'IP' :
			camurl='http://'+paramval['cameraip']+':'+paramval['cameraport']+'@'+paramval['camerauser']+':'+paramval['camerapwd']+'/'+paramval['cameraurl']
			cap = cv2.VideoCapture(camurl)  #arpan
		if paramval['camera'].upper() == 'WEB' :
			cap = cv2.VideoCapture(0)
	elif paramval['camerastream'] == 'rtsp':
		if paramval['camera'].upper() == 'IP' :
			camurl='rtsp://'+paramval['camerauser']+':'+paramval['camerapwd']+'@'+paramval['cameraip']+'/'+paramval['cameraurl']
			cap = IPCamera(camurl) 
		elif paramval['camera'].upper() == 'CSI':
			cap = CSICamera(width=224, height=224)
		elif paramval['camera'] == 'USB':
			cap = USBCamera(capture_device=-1)
		cap.running = True

cap.set(cv2.CAP_PROP_FPS,10)
time.sleep(1.0)

# ---------------------------------------------------------------------------------------------------

global score

# ---------------------------------------------------------------------------------------------------
#Change FPS and padding

WINDOW_NAME = 'Video Gesture Recognition'

def main():
	global buffer, gesans,vexecutor,vctx,feat,transform, lfile,oimap
	print("Open camera...")

	# env variables
	print("Ready! ")

	inputx = 'http://'+paramval['device'] + ':'+paramval['port']


	lnl=0
	lfile='question_2022_jun.json'
	f = open(lfile,"r")
	datal = json.load(f)	
	for i in datal["questions"]:  
		oln=0
		
		for j in i["options"]:
			imgurl=datal["questions"][lnl]["options"][oln]["image"]["image"]
			print("imgae url : " , imgurl)
			oimap[datal["questions"][lnl]["options"][oln]["value"]]=datal["questions"][lnl]["options"][oln]["image"]["name"]
			oln=oln+1
		lnl=lnl+1
	print("Map ",oimap)
		


# ---------------------------------------------------------------------------------------------------

@app.route("/")
def index():
	global lfile
	#f = open('Data.json',)
	#data = json.load(f)
	#for i in data['questions']:
	#	lst.append(i)
	#f.close()
	
	return render_template("index.html")


@app.route("/video_feed")
def video_feed():
	""" Return the response generated along with the specific media type (mime type) """
	return (Response(model_process.analyze(cap), mimetype="multipart/x-mixed-replace; boundary=frame"))



@app.route("/survey_start", methods=["POST", "GET"])
def survey_start():
	lval=[]
	nl=[]
	start_survey= False	
	question=None	
	global lst, ln, gesans, sess, lfile
	lst=[]
	ln=0
	gans=None
	lw=string.ascii_lowercase

	sess ="".join(random.sample(lw,10))  

	print("survey_start : ", sess)
	
	if request.method == "POST":
		loc = request.form["location"]


	f = open(lfile,"r")
	data = json.load(f)

		
	for i in data["questions"]:  
		nl.append(i)
		ln=ln+1

	lst=nl

	f.close()

	
	
	gans=''
	gjson={}

	while True :
		gjson=model_process.get_gesture_text()   #maintemporal()
		gans = gjson["sign"]
		print("First Gesture : ", gans)
		if gans=="Thumbs Up" :
			start_survey = True
			break
		time.sleep(0.3)						
	gesans = ''
	return jsonify({"start_survey":start_survey,
		'question' : question , "gesture" : gans, "ansimage" : "Thumbs Up.png"
	})

@app.route("/survey", methods=['POST', 'GET'])
def survey():
	lval=[]
	nl=[]
	ansfinal={}
		
	survey_status=None
	question=None
	dt=None
	tm=None
	qstr="dummy"

	global lst, ln, gesans, df,sess,hostname, qmode
	gans1=""
	gtmp=""
	print("survey")
	
	if request.method == "POST":
		qstate = int(request.form["state"])  #data = request.get_json()
		#usr = request.form['user']
		rconf= request.form["receive_confirmation"]
		ques=request.form["question"]

		print("Gesture ok ques : ", ques)
	#print("Request conf : ", rconf)
	dt=format(datetime.datetime.today().date(),"%Y-%m-%d")
	tm=format(datetime.datetime.today().time(),"%H:%M:%S")


	if rconf == "ok" :
		gans1=""
		ansjson={}

		while True:
			ansjson=model_process.get_gesture_text()   #maintemporal()
			if qmode == "Gesture":
				gans1=ansjson["sign"]
				if gans1 in ["Thumbs Up", "Thumbs Down","Neutral" , "Stop"] :
					break		
			elif qmode == "Count":
				gtmp=ansjson["count"]
				if gtmp in ["1","2","3","4","5" ] :
					gans1=lst[int(ques)-1]["options"][int(gtmp)-1]["value"]   # Change on Nov 27 based on Json structure gans1=lst[i\nt(ques)-1]["options"][int(gtmp)-1]
					#gansimg=lst[int(ques)-1]["options"][int(gtmp)-1]["image"]["name"] 
					break	 		
			time.sleep(0.3)	
		print("Gesture ok : ", gans1)


		if qstate <= ln:
			if gans1 == "Stop":
				survey_status = "complete"
				question = "Thank you"
				gcpdata[qstr]=gans1
				ansfinal=surveyend(dt,tm)
				print(ansfinal,end="\n")
			else :	
				survey_status = "ongoing"
				question = lst[qstate - 1]
				qstr=question["question"][0]['text']    # Nov 19 bu Subham : question["q1"]
				qmode=question["aiType"]     # Nov 19 bu Subham : question["qmode"]
				print("qmode ",qmode)
				print("Ques : ",qstr)
				gcpdata[qstr]=gans1

		else :
			survey_status = "complete"
			question = "Thank you"
			gcpdata[qstr]=gans1
			gesans=""
			ansfinal=surveyend(dt,tm)  # data to transferred to firebase
			print(ansfinal,end="\n")		
			sendToQ(ansfinal)	

	
	time.sleep(2)

	gesans=None
	ansimg=None
	ansimg=oimap[gans1]
	return jsonify({"survey_status":survey_status,
		"question" : question , "gesture" : gans1, "ansimage" : ansimg
	})


def sendToQ(ansfinal):

	lfile=sess+".json"
	with open(lfile, "w") as ofile:
    		ofile.write(json.dumps(ansfinal)) 
    		
    		print("dump du Json de reponse",json.dumps(ansfinal))


def surveyend(dt,tm):
	lst=list(gcpdata.items())
	nd={"HostNumber":hostsrl,"Name":sess,"Date":dt,"Time":tm}
	#print(lst,end='\n')
	for i in range (0,len(lst)-1):
    		nd[lst[i][0]]=lst[i+1][1]
	
	gcpdata.clear()
	return nd

# @app.route("/log")
# def log():
# 	new_lst=detect_motion_core()
# ===================================================================================================

# Check to see if this is the main thread of execution
if __name__ == '__main__':


	# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
	# Construct the argument parser and parse command line arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--device_ip",
					type=str,
					default=os.environ.get('DEVICE_IP', "127.0.0.1"),
					help="ip address of the local device (127.0.0.1 means listen on all public IPs)")

	ap.add_argument("-o", "--server_port",
					type=int,
					default=int(os.environ.get('SERVER_PORT', "5000")),
					help="ephemeral port number of the server (1024 to 65535)")
	args = vars(ap.parse_args())
	'''
	########## generate qr code background ###########
	if GenerateQrCode.CreateQR(1):
		backgroundQr = GenerateQrCode.GetQrBackground()
		backgroundQr.save("./static/images/qrBackground.jpg")
	else:
		logging.error("Unable to generate QR Background")
	'''

	# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

	print("main - singlethread") 
	main()
	
	# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
	# Start the flask app
	app.run(host=args["device_ip"],
			port=args["server_port"],
			debug=True,
			threaded=True,
			use_reloader=False)

	# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
	# Release the video stream pointer
	if paramval['camerastream'] == 'rtsp':
		cap.running = False
	elif paramval['camerastream'] == 'http':
		cap.release()


