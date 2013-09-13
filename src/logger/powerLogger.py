#!/usr/bin/python
import RPi.GPIO as GPIO
import time, threading
from datetime import datetime
import sys,os, sched

# setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)
#raw_input("Press Enter when ready\n>")

imps=0
timer=None
logInterval=60*10


def logResult():
	global imps
	global timer
	global logInterval
	fileName='power_data.csv'
	f=open(fileName,'a')	
	t=datetime.now()		
	outStr= '%s,%s,%s,%s,%s,%s,%s' % (t.year, t.month, t.day, t.hour,t.minute, t.second,imps) 
	f.write(outStr + '\n')
	print 'impulses: ' + str(imps)
	imps=0
	f.close()
	if logInterval>0:
		timer=threading.Timer(logInterval,logResult)
		timer.start()

try:
	logResult()
	while 1:
		GPIO.wait_for_edge(23, GPIO.FALLING)
		imps=imps+1
		time.sleep(0.5)
		print 'imp logged!'


except (KeyboardInterrupt, SystemExit):
	GPIO.cleanup()       # clean up GPIO on CTRL+C exit
	logInterval=0
GPIO.cleanup()           # clean up GPIO on normal exit
logInterval=0

