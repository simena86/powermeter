#!/usr/bin/python
import platform
from selenium.webdriver.common.keys import Keys
import urllib
import re
import requests
import sys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from lxml import etree, html
import StringIO
from selenium import webdriver
import time
import struct
import os

def dataToCSVLine(date,data,index):
	ret=''
	dates=date.split('-')
	for a in dates:
		ret= a + ',' + ret  
	ret=ret + str(index) + ", 00, " + str(data)
	return ret

def dataToTemp(raw):
	temp=raw.split(",")
	nr1=temp[0]
	nr2=temp[1]
	nr2=nr2[0:1]
	return nr1+"."+nr2

# get temperature data from website. historical measurement
# from voll in trondheim
def getTemperatureData():
	url="http://www.yr.no/sted/Norge/S%C3%B8r-Tr%C3%B8ndelag/Trondheim/V%C3%A6re/almanakk.html"
	page = html.fromstring(urllib.urlopen(url).read())
	tempDate=page.xpath('//p[@class="day-of-year"]/text()')
	tempDate=tempDate[0].split(' ')
	tempDate= tempDate[0].split('.')
	date=[]
	for itm in tempDate:
		date.append(str(int(itm)))
	data=[]
	xpath='//table[@class="yr-table yr-table-hourly yr-popup-area"]'
	for row in page.xpath(xpath):
		for col in row.xpath('//td[position()=2]/text()'):
			filtered=re.sub("[^0-9,\.]","",col)
			if filtered.strip()!="":
				data.append(dataToTemp(str(filtered)))
	outData=[]		
	for itm in range(24):
		outData.append(date[::-1]+[str(itm),'0','0',str(data[itm])])
	return outData

# gets the value of a nok in euros from daz web
def euros2NOK(browser):
	user_agent = (
	    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) " +
		 "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"
	)
	dcap = dict(DesiredCapabilities.PHANTOMJS)
	dcap["phantomjs.page.settings.userAgent"] = user_agent
	URL='http://themoneyconverter.com/NOK/EUR.aspx'
	browser.get(URL)
	time.sleep(0.1)
	page=html.fromstring(browser.page_source)
	euros=browser.find_element_by_id("ratebox").text
	euros = re.sub("[^0-9]", "", euros)
	euros=euros[0:1] + "." + euros[1:]
	nok=1/float(euros)
	return nok

# get the data from nordpoolspot.com for trondheim. 
# data is fetched from website
def getPriceData(day='today'):
	dst=platform.dist()
	if dst[0]=='Ubuntu':
		if struct.calcsize("P")*8==64:
			phantomjs='./phantomjs_64b'
		else:
			phantomjs='./phantomjs_acer'
	else:
		print 'phantomjs for raspberry'
		phantomjs='./phantomjs_raspberry'
	user_agent = ( "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) " +
		 "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"	)
	dcap = dict(DesiredCapabilities.PHANTOMJS)
	dcap["phantomjs.page.settings.userAgent"] = user_agent
	URL='http://www.nordpoolspot.com/Market-data1/Elspot/Area-Prices/ALL1/Hourly/'
	browser = webdriver.PhantomJS(executable_path=phantomjs,desired_capabilities=dcap)
	nok=euros2NOK(browser)
	browser.get(URL)
	page=html.fromstring(browser.page_source)
	tempDate= page.xpath('//tr[@class="rgGroupHeader"]//p/text()')
	nextId="ctl00_FullRegion_npsGridView_lnkNext"
	time.sleep(1)
	optLstName="ctl00$FullRegion$npsActionPanelView$ddlEntities" 
	lst=browser.find_element_by_name(optLstName)
	for option in lst.find_elements_by_tag_name('option'):
		if option.text==' Tr.heim':
			option.click()
			break
	time.sleep(1)
	page = html.fromstring(browser.page_source)
	browser.close()
	tempDate=tempDate[0].split('-')
	dayMonthYear=''
	for itm in tempDate:
		dayMonthYear=itm+","+dayMonthYear
	data=[]
	xpath='//table[@id="ctl00_FullRegion_npsGridView_trkGrid_ctl00"]//tbody'
	index =0
	if day=='today':
		column=3
	elif day=='yesterday':
		column=4
	else:
		print 'Wrong argument to getPriceData. Must be yesterday or today. Using today'
		column=3
	for row in page.xpath(xpath):
		for col in row.xpath('//td[position()='+str(column)+']/text()'):
			if index>24:
				break
			elif not re.search('[a-zA-Z]', str(col)):
				data.append(col)
			index=index+1
	outData=[]
	for itm in range(24):
		price=float(data[itm].replace(',','.'))*nok*0.001
		price=round(price,3)
		outData.append(tempDate[::-1]+[str(itm),'0','0',str(price)])
	return outData

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

# update the data files with the new data
def updateTempAndPriceData():
	tempFile='temperature_data.csv'
	priceFile='price_data.csv'
	tempLst=getTemperatureData()
	priceLst= getPriceData()
	tempDataFileLst=csvFile2Array(tempFile)
	priceDataFileLst=csvFile2Array(priceFile)
	priceRow=0
	tempRow=0
	tempDataFileLst=removeZerosFromTempData(tempDataFileLst)	
	for row in tempLst:
		date=row[:6]	
		temp=row[6]
		tempDataFileLst.append(date+[temp])
		tempRow=tempRow+1

	for row in priceLst:
		date=row[:6]
		price=row[6]
		priceDataFileLst.append(date+[price])
		tempDataFileLst.append(date+[0])
		priceRow=priceRow+1

	tempDataFileLst=removeOldDataFromFile(tempDataFileLst)
	priceDataFileLst=removeOldDataFromFile(priceDataFileLst)
	writeArrayToCSVFile(tempDataFileLst,tempFile)
	writeArrayToCSVFile(priceDataFileLst,priceFile)

# remove old data
def removeOldDataFromFile(dataArr):
	maxDataSamplesPerFile=24*3
	arrLen=len(dataArr)	
	if maxDataSamplesPerFile>arrLen:
		return dataArr
	for i in range(arrLen-maxDataSamplesPerFile):
		dataArr.pop(0)
	return dataArr


# remove the 24 zero rows at end of temperature data
def removeZerosFromTempData(tempData):
	if not len(tempData)<23:
		for i in range(24):
			tempData.pop()
	return tempData


# write array to a csv formatted file called 'filename'
def writeArrayToCSVFile(array,fileName):
	f=open(fileName,'w')
	line=''
	for row in array:
		for itm in row:
			line=line + str(itm) + ',' 
		f.write(line[:-1]+'\n')	# remove the last comma
		line=''


updateTempAndPriceData()



























