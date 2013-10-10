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
			try:
				f=open(file,'r')
				nr=f.readline()
				f.close()
			except:
				print "could not read from file"
				nr=0
				f.close()
			nr=int(nr)
			imps=nr+1
			try:
				f=open(file,'w')
				f.write(str(imps))
				f.close()
			except:
				print "could not write to powerTemp"

			time.sleep(0.4)

	except KeyboardInterrupt, e:
		print(e)
		f.close()	
		GPIO.cleanup()       # clean up GPIO on CTRL+C exit
		exit(0)	
	except SystemExit,e:
		print e
		f.close()
		GPIO.cleanup()       # clean up GPIO on CTRL+C exit
		print "system exit"
	except Exception, e:
		print e
		f.close() 	
		GPIO.cleanup()       # clean up GPIO on CTRL+C exit
		
GPIO.cleanup()           # clean up GPIO on normal exit

