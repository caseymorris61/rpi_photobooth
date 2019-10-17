from time import sleep, strftime
from picamera import PiCamera
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from PIL import Image


class PhotoBooth:

	def __init__(self,id_in="VOID"):
		self.camera = PiCamera()
		#self.camera.resolution = (1024, 768)
		self.camera.resolution = (1640, 1232)
		self.fid=id_in
		self.camera.rotation = 270
		image1 = Image.open("overlay.png")
		print "Creating Overlay"
		pad1 = Image.new("RGB", (
			((self.camera.resolution[0]+31)//32)*32,
			((self.camera.resolution[1]+15)//16)*16,
			))
		print "Pasting Image"
		pad1.paste(image1,(0,0))
		print "Adding Overlay"
		self.camera.add_overlay(pad1.tobytes(),alpha=64,layer=3)
		print "Starting Preview"
		self.camera.annotate_text="Text 'Snap' to  <Phone Number> to start countdown!"
		self.gauth = GoogleAuth()
		self.gauth.LocalWebserverAuth()
		self.drive = GoogleDrive(self.gauth)
		print "Ready"
		self.camera.start_preview()



	def takePicture(self):
		#self.camera.start_preview()
        self.camera.annotate_text="5"
    	sleep(1)
        self.camera.annotate_text="4"
    	sleep(1)
        self.camera.annotate_text="3"
    	sleep(1)
    	self.camera.annotate_text="2"
    	sleep(1)
    	self.camera.annotate_text="1"
    	sleep(1)
    	self.camera.annotate_text=""
    	outfilename = "SpecialName_img_"+strftime("%m%d%Y_%I%M%S")+".jpg"
		self.camera.capture(outfilename)
		self.camera.annotate_text="Uploading.....Please wait"
		if "VOID" in self.fid:
			file1 = self.drive.CreateFile()
		else:
			file1 = self.drive.CreateFile({"parents":[{"kind": "drive#fileLink","id":self.fid}]})

		file1.SetContentFile(outfilename)
		file1.Upload()
		permission = file1.InsertPermission({
					'type': 'anyone',
					'value': 'anyone',
					'role': 'reader'})
		print 'Image uploaded: '+file1['alternateLink']
		#self.camera.stop_preview()
		self.camera.annotate_text="Text 'Snap' to <Phone Number> to start countdown!"
		return file1['alternateLink']

	def closePhotobooth(self):
		self.camera.close()




