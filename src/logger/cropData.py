#!/usr/bin/python
import os

# read data from a csv file and return an array 
# containing the data
def csvFile2Array(fileName):
	if not os.path.exists(fileName):
		return []
	data=[]
	i=0
	# open file and thus creating it if it does not exist already
	#f=open(fileName,'w')
	#f.close()
	f=open(fileName,'r')
	for line in f:
		data.append([])
		for itm in line.split(','):
			itm=itm.replace('\n','')
			data[i].append(itm)
		i=i+1
	f.close()
	return data

# remove old data
def removeOldDataFromFile(dataArr):
	maxDataSamplesPerFile=6*24*14
	arrLen=len(dataArr)	
	if maxDataSamplesPerFile>arrLen:
		return dataArr
	for i in range(arrLen-maxDataSamplesPerFile):
		dataArr.pop(0)
	return dataArr

# write array to a csv formatted file called 'filename'
def writeArrayToCSVFile(array,fileName):
	f=open(fileName,'w')
	line=''
	for row in array:
		for itm in row:
			line=line + str(itm) + ',' 
		f.write(line[:-1]+'\n')	# remove the last comma
		line=''

def cropData():
	file='/home/pi/powermeter/src/logger/power_data.csv'
	data=csvFile2Array(file)
	data=removeOldDataFromFile(data)
	writeArrayToCSVFile(data,file)

cropData()	
	



