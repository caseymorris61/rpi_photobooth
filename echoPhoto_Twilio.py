from flask import Flask, request
from flask_ask import Ask, statement, convert_errors
from photoBooth import PhotoBooth
import logging

from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

account='Twilio Account'
auth_token='Twilio Auth Token'
client = Client(account,auth_token)

app = Flask(__name__)
ask = Ask(app, '/')
folder_id = "Folder ID google drive"
booth = PhotoBooth(folder_id)

#For Alexa intent
@ask.intent('PhotoIntent')
def takePhoto():
	print "Taking Picture"
	media = booth.takePicture()
	return statement('Picture Taken and uploaded to Google Drive')


@app.route('/sms', methods=['GET', 'POST'])
def takePhotoAndReply():
	body = request.values.get('Body',None)
	msg = MessagingResponse()
	if "Snap" in body or "snap" in body:
		print "Taking Picture"
		media = booth.takePicture()
		txt='#WeddingHashtag %s' % media
	elif "photoboothexit" in body or "Photoboothexit" in body:
		booth.closePhotobooth()
		txt = "Thank you for using Photobooth"
	else:
		txt = "Text Not Recognized. Reply 'Snap' to start countdown"
	msg.message(txt)
	return str(msg)

#Take picuture via http request 
@app.route('/web')
def snapPicture():
	media = booth.takePicture()
	outStr = "Picture taken! \r\n \n%s" % media
	return outStr

