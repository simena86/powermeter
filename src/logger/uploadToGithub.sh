#!/bin/bash

i=`ps -e | grep -c "uploadToGithub"`

if [ "$i" -gt 2 ] 
then
	echo "this program is already running"
	exit
fi

echo "rm -rf /home/pi/powermeter_web_page/github_pages"
rm -rf /home/pi/powermeter_web_page/github_pages
echo "git clone git@github.com:simena86/simena86.github.com.git /home/pi/powermeter_web_page/github_pages"
git clone git@github.com:simena86/simena86.github.com.git /home/pi/powermeter_web_page/github_pages

# copy files from data fetch to 
cp /home/pi/powermeter/src/logger/power_data.csv /home/pi/powermeter_web_page/github_pages/powermeter/data/
cp /home/pi/powermeter/src/logger/price_data.csv /home/pi/powermeter_web_page/github_pages/powermeter/data/
cp /home/pi/powermeter/src/logger/temperature_data.csv /home/pi/powermeter_web_page/github_pages/powermeter/data/

cd /home/pi/powermeter_web_page/github_pages/

echo "git add /home/pi/powermeter_web_page/github_pages/powermeter/data/*"
git add /home/pi/powermeter_web_page/github_pages/powermeter/data/*
echo "git commit -m "committing from raspberry pi""
git commit -m "committing from raspberry pi"
echo "git push origin master"
git push origin master 

