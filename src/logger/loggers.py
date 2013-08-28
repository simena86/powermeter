#!/usr/bin/python
import platform
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
def getPriceData():
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
	nextBtn=browser.find_element_by_id(nextId)
	time.sleep(0.1)
	nextBtn.click()
	time.sleep(0.1)
	page = html.fromstring(browser.page_source)
	browser.close()
	tempDate=tempDate[0].split('-')
	dayMonthYear=''
	for itm in tempDate:
		dayMonthYear=itm+","+dayMonthYear
	data=[]
	xpath='//table[@id="ctl00_FullRegion_npsGridView_trkGrid_ctl00"]'
	index =0
	column=5
	for row in page.xpath(xpath):
		for col in row.xpath('//td[position()='+str(column)+']/text()'):
			index=index+1
			if index>24:
				break
			elif index>0:
				data.append(col)
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
	f=open(fileName,'r')
	for line in f:
		data.append([])
		for itm in line.split(','):
			itm=itm.replace('\n','')
			data[i].append(itm)
		i=i+1
	f.close()
	return data

def updateTempAndPriceData():
	tempLst=getTemperatureData()
	priceLst= getPriceData()
	fileName='tempAndPrice.csv'
	f=open(fileName,'w')
	f.close()
	dataFromFile=csvFile2Array(fileName)
		

updateTempAndPriceData()


