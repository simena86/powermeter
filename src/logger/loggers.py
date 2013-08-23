#!/usr/bin/python
import urllib
from lxml import etree, html
import StringIO
import urllib
import re

def dataToCSVLine(date,data,index):
	ret=''
	dates=date.split('-')
	for a in dates:
		ret= a + ',' + ret  
	ret=ret + str(index) + ", 00, " + str(data)
	return ret

def getSpotPriceData():
	path='spot.html'
	parser=etree.HTMLParser()
	tree=etree.parse(path,parser)
	xpath='//table[@id="ctl00_FullRegion_npsGridView_trkGrid_ctl00"]'
	root = tree.xpath(xpath)
	d=tree.xpath(xpath + '//tr[position()=1]//td[position()=1]/text()')
	date=d[0]
	trHeimColIndex=14
	data=[]
	for row in root:
		for col in row.xpath('//td[position()='+str(trHeimColIndex)+']/text()'):
			data.append(col)
		
	out=open('price_data.csv','w')
	for itm in range(24):
		out.write( dataToCSVLine(date,data[itm],itm))
		out.write('\n')
	out.close()

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

def getPriceData():
	url="http://www.nordpoolspot.com/Market-data1/Elspot/Area-Prices/ALL1/Hourly/"
	page = html.fromstring(urllib.urlopen(url).read())
	tempDate=page.xpath('//tr[@class="rgGroupHeader"]//p/text()')
	tempDate=tempDate[0].split('-')
	dayMonthYear=''
	for itm in tempDate:
		dayMonthYear=itm+","+dayMonthYear
	data=[]
	xpath='//table[@id="ctl00_FullRegion_npsGridView_trkGrid_ctl00"]'
	index =0
	for row in page.xpath(xpath):
		for col in row.xpath('//td[position()=14]/text()'):
			if index>23:
				break
			index=index+1
			print col
			data.append(col)
	print index	
	out=open('price_data.csv','w')
	for itm in range(24):
		out.write(dayMonthYear+str( itm)+",0,0,"+str(data[itm] ))
		out.write('\n')
	out.close()
