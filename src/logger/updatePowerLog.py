#!/usr/bin/python
import time
from datetime import datetime

def updateLog():
	try:
		tmpFileName='/home/pi/powermeter/src/logger/powerTemp'
		f=open(tmpFileName,'r')
		nr=f.readline()
		f.close()
		f=open(tmpFileName,'w')
		f.write('0')
		f.close()
	except Exception,e:
		print e
		f.write('0')
		f.close()
	try:
		nr
	except:
		nr=0
	try:
		fileName='/home/pi/powermeter/src/logger/power_data.csv'
		f=open(fileName,'a')	
		t=datetime.now()		
		outStr= '%s,%s,%s,%s,%s,%s,%s' % (t.year, t.month, t.day, t.hour,t.minute, t.second,nr) 
		f.write(outStr + '\n')
		f.close()
	except Exception, e:
		print e
		f.close()

updateLog()
