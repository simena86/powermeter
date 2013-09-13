#!/usr/bin/python
import RPi.GPIO as GPIO
import time, threading
from datetime import datetime
import sys,os, sched

# setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)

imps=0



try:
	file='./powerTemp'
	while 1:
		GPIO.wait_for_edge(23, GPIO.FALLING)
		print 'edge detected'
		f=open(file,'r')
		nr=f.readline()
		f.close()
		nr=int(nr)
		imps=nr+1
		f=open(file,'w')
		print 'nr: '  + str(nr)
		f.write(str(imps))
		f.close()
		time.sleep(0.4)
		print 'imp logged!'
		


except (KeyboardInterrupt, SystemExit):
	f.close()	
	GPIO.cleanup()       # clean up GPIO on CTRL+C exit
GPIO.cleanup()           # clean up GPIO on normal exit

