#!/usr/bin/python
import RPi.GPIO as GPIO
import time, threading
from datetime import datetime
import sys,os, sched

while 1:
	try:
		# setup GPIO
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(23, GPIO.IN)
		imps=0
		file='./powerTemp'
		f=open(file,'w')
		f.write(str(0))
		f.close()
		while 1:
			GPIO.wait_for_edge(23, GPIO.FALLING)
			f=open(file,'r')
			nr=f.readline()
			f.close()
			nr=int(nr)
			imps=nr+1
			f=open(file,'w')
			f.write(str(imps))
			f.close()
			time.sleep(0.4)

	except (KeyboardInterrupt):
		f.close()	
		GPIO.cleanup()       # clean up GPIO on CTRL+C exit
		exit(0)	
	except SystemExit:
		f.close()
		GPIO.cleanup()       # clean up GPIO on CTRL+C exit
		print "system exit"
	except:
		f.close() 	
		GPIO.cleanup()       # clean up GPIO on CTRL+C exit
		
GPIO.cleanup()           # clean up GPIO on normal exit

