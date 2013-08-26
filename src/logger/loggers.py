#!/usr/bin/python
import urllib
import re
import requests
import sys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from lxml import etree, html
import StringIO
from selenium import webdriver
import time

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

def getTemperatureData():
	url="http://www.yr.no/sted/Norge/S%C3%B8r-Tr%C3%B8ndelag/Trondheim/V%C3%A6re/almanakk.html"
	page = html.fromstring(urllib.urlopen(url).read())
	tempDate=page.xpath('//p[@class="day-of-year"]/text()')
	tempDate=tempDate[0].split(' ')
	dayMonthYear=''
	for itm in tempDate[0].split('.'):
		dayMonthYear=itm+","+dayMonthYear
	data=[]
	xpath='//table[@class="yr-table yr-table-hourly yr-popup-area"]'
	for row in page.xpath(xpath):
		for col in row.xpath('//td[position()=2]/text()'):
			filtered=re.sub("[^0-9,\.]","",col)
			if filtered.strip()!="":
				data.append(dataToTemp(str(filtered)))
		
	out=open('temperature_data.csv','w')
	for itm in range(24):
		out.write(dayMonthYear+str( itm)+",0,0,"+str(data[itm] ))
		out.write('\n')
	out.close()

# get the data from nordpoolspot.com for trondheim. data is fetched from website
def getPriceData():
	user_agent = (
	    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) " +
		 "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"
	)
	dcap = dict(DesiredCapabilities.PHANTOMJS)
	dcap["phantomjs.page.settings.userAgent"] = user_agent
	URL='http://www.nordpoolspot.com/Market-data1/Elspot/Area-Prices/ALL1/Hourly/'
	browser = webdriver.PhantomJS(executable_path='./phantomjs',desired_capabilities=dcap)
	browser.get(URL)
	page=html.fromstring(browser.page_source)
	tempDate= page.xpath('//tr[@class="rgGroupHeader"]//p/text()')
	nextId="ctl00_FullRegion_npsGridView_lnkNext"
	nextBtn=browser.find_element_by_id(nextId)
	time.sleep(1)
	nextBtn.click()
	time.sleep(1)
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
				print col
				data.append(col)
	out=open('price_data.csv','w')
	for itm in range(24):
		out.write(dayMonthYear+str( itm)+",0,0,"+str(data[itm] ).replace(',','.'))
		out.write('\n')
	out.close()
