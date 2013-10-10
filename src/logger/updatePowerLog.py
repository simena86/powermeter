#!/usr/bin/python
import time
from datetime import datetime

def updateLog():
	try:
		tmpFileName='/home/pi/powermeter/src/logger/powerTemp'
		powerFileName='/home/pi/powermeter/src/logger/power_data.csv'
		f=open(tmpFileName,'r')
		nr=int(f.readline())
		f.close()	
	except Exception,e:
		print e
		f.close()
	try:
		f=open(tmpFileName,'w')
		f.write('0')
		f.close()
	except:
		f.close
	try:
		f=open(powerFileName,'a')	
		t=datetime.now()		
		outStr= '%s,%s,%s,%s,%s,%s,%s' % (t.year, t.month, t.day, t.hour,t.minute, t.second,nr) 
		f.write(outStr + '\n')
		f.close()
	except Exception, e:
		print e
		f.close()

updateLog()
