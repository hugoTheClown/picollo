from picamera import PiCamera
from picamera import Color
from time import sleep
from datetime import datetime
from fpdf import FPDF
from PIL import Image

import cups
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

buttonPIN = 40;
GPIO.setup(buttonPIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

camera = PiCamera()
camera.rotation = 180
# camera.resolution = (2592, 1944)
camera.resolution = (1280, 720)
camera.start_preview()

timingRange = 3
timing = []

for i in range(timingRange+1):
    img = Image.open('overlays/o%d.png' % (i + 1))

    pad = Image.new('RGB', (
      ((img.size[0] + 31) // 32) * 32,
      ((img.size[1] + 15) // 16) * 16,
      ))

    pad.paste(img, (0, 0))
    o = camera.add_overlay(pad.tobytes(), size=img.size)
    o.alpha = 0
    o.layer = 0
    timing.insert(0, o)
    print(i)

def hideOverlays():
    for j in range(timingRange+1):
        timing[j].layer = 0
        timing[j].alpha = 0

def showOverlay(k):
    timing[k].layer = 3
    timing[k].alpha = 16    #128

conn = cups.Connection()
n = -5

imx = 107
imy = 85

isx = (150-imx)/2
isy = (100-imy)/2+2

def createPDF(today):
	pdffilename = '/home/clown/picollo/pixs/%s_picollo.pdf' % (today)
	imageName = '/home/clown/picollo/pixs/%s_picollo.jpg' % (today)
	pdf = FPDF('L', 'mm', (100,150))
	pdf.add_page()
	pdf.set_font('Times', '', 14)
	
	with pdf.rotation(90):
		pdf.text(-75, 20, "E&H, 3. 9. 2022")

		
	pdf.image(imageName,isx,isy,imx,imy)	
	pdf.output(pdffilename)


def shootPicture(today):
	filename = '/home/clown/picollo/pixs/%s_picollo.jpg' % (today)	
	camera.capture(filename)
	camera.stop_preview()

#while True: # Run forever
while n<0: # Run forever
	buttonInput = GPIO.input(buttonPIN)
	if buttonInput == GPIO.LOW:
		print("Button was pushed!")
		timeout = 0
		while timeout<timingRange:
			showOverlay(timeout+1)
			sleep(1)
			timeout+=1
			hideOverlays()
		today = datetime.today().strftime("%Y%m%d_%H%M%S");
		# today="TEST";
		shootPicture(today);
		createPDF(today);
		# conn.printFile("canon7200", '/home/clown/picollo/pixs/%s_picollo.pdf' % (today),"hura",{})		 
		# while conn.getJobs():
			
		camera.start_preview()
		hideOverlays()
		n+=1


hideOverlays()
camera.stop_preview()






