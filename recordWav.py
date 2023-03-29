# Poetry Wall 1.0
# Record WAV example

import sys
import requests
import uuid
import os
import time

# settings
recordingTime=10
imageSeconds=15
loopSeconds=15
debugMode=1
usbMicCard=1

# main program

while True:

	filename = str(uuid.uuid4())
	
	os.system("arecord -D plughw:"+str(usbMicCard)+",0 --duration="+str(recordingTime)+" "+filename+".wav")

	if debugMode==1:
		print("Waiting to restart...")

	time.sleep(loopSeconds)
