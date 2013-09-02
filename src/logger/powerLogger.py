import RPi.GPIO as GPIO
import time, threading
from datetime import datetime

# setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)
raw_input("Press Enter when ready\n>")

imps=0

def logResult():
	global imps
	fileName='power_data.csv'
	f=open(fileName,'a')	
	t=datetime.now()		
	outStr= '%s,%s,%s,%s,%s,%s,%s' % (t.year, t.month, t.day, t.hour,t.minute, t.second,imps) 
	f.write(outStr + '\n')
	print 'impulses: ' + str(imps)
	imps=0
	f.close()
	logInterval=60*10
	threading.Timer(logInterval,logResult).start()

try:
	logResult()
	while 1:
		GPIO.wait_for_edge(23, GPIO.FALLING)
		imps=imps+1
		print 'imp logged!'


except KeyboardInterrupt:
	GPIO.cleanup()       # clean up GPIO on CTRL+C exit
	thread.exit()
GPIO.cleanup()           # clean up GPIO on normal exit
