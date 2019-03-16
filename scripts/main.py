# -*- coding: utf-8 -*-
"""
This script will be retrieve weather from accuweather and
send alert messages to all friends in facebook.

Note: all related files (keys.py,params.py,main.py) should be stored in the same folder.
"""
###############################################################################
#set the current directory
import os
os.chdir(r".\YOUR_PATH")
###############################################################################
#import keys and parameters other scripts in the same folder
from keys import FB_USERNAME,FB_PASSWORD,ACCUWEATHER_API_KEY
from params import RAIN_THRESHOLD,SNOW_THRESHOLD,UPDATE_INTERVAL_HR,DELAY_TIME_HR,LOCATION_ID
###############################################################################
#import required modules
import urllib
import urllib.parse
import json
import time
import requests
import pandas as pd
import logging
import sys
from fbchat import Client
from fbchat.models import *
from datetime import datetime
####################################################################################################
url_page = "http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/"+str(LOCATION_ID)+"?apikey="+ACCUWEATHER_API_KEY+"&details=true&metric=true"
#convert hours to seconds
update_interval_sec = 60*60*UPDATE_INTERVAL_HR 
delay_time_sec = 60*60*DELAY_TIME_HR 
###############################################################################
# Request and extract json function
def func_get_weather(url_page):

    json_page = urllib.request.urlopen(url_page)
    json_data = json.loads(json_page.read().decode())
    json_df = pd.DataFrame(json_data)
    
    # set maximum width, so the links are fully shown and clickable
    pd.set_option('display.max_colwidth', -1)
    json_df['Links'] = json_df['MobileLink'].apply(lambda x: '<a href='+x+'>Link</a>')
    
    json_df['Real Feel (degC)'] = json_df['RealFeelTemperature'].apply(lambda x: x.get('Value'))
    json_df['Weather'] = json_df['IconPhrase'] 
    json_df['Percent_Rain'] = json_df['RainProbability'] 
    json_df['Percent_Snow'] = json_df['SnowProbability'] 
    json_df[['Date','Time']] = json_df['DateTime'].str.split('T', expand=True)
    # trim the time to hh:mm format, change to str
    json_df[['Time']] = json_df['Time'].str.split('+', expand=True)[0].astype(str).str[:5]
    
    current_retrieved_datetime = str(json_df['Date'][0])+' '+str(json_df['Time'][0])
    
    rain_msg=""
    snow_msg=""
    
    # check % Rain column, return rain_msg
    json_df.loc[json_df['Percent_Rain'] >= RAIN_THRESHOLD, 'Rain_Alert'] = 1  
    json_df.loc[json_df['Percent_Rain'] < RAIN_THRESHOLD, 'Rain_Alert'] = 0
    if (sum(json_df['Rain_Alert']) > 0):
        rain_msg = 'There is ' \
                    +str(json_df['Percent_Rain'][json_df['Rain_Alert']==1][0]) \
                    +' % chance of rain' \
                    +' at ' \
                    +str(json_df['Time'][json_df['Rain_Alert']==1][0])
    
    # check % Snow column
    json_df.loc[json_df['Percent_Snow'] >= SNOW_THRESHOLD, 'Snow_Alert'] = 1  
    json_df.loc[json_df['Percent_Snow'] < SNOW_THRESHOLD, 'Snow_Alert'] = 0
    if (sum(json_df['Snow_Alert']) > 0):
        snow_msg = 'There is ' \
                    +str(json_df['Percent_Snow'][json_df['Percent_Snow']==1][0]) \
                    +' % chance of snow' \
                    +' at ' \
                    +str(json_df['Time'][json_df['Percent_Snow']==1][0])

    alert_msg =""
    if(len(rain_msg)|len(snow_msg)!=0):
         alert_msg = rain_msg +" "+snow_msg
    
    link_for_click = json_df['MobileLink'][0]
    
    return(current_retrieved_datetime,alert_msg,link_for_click)
####################################################################################################
# Execute functions, retrieve data and send facebook msg
num_repeat = 999 # number of loops to repeat
previous_alert_msg = "" # initialize alert msg
for i in range(num_repeat):
    
    try:
        current_retrieved_datetime,alert_msg,link_for_click = func_get_weather(url_page)
    except (RuntimeError, TypeError, NameError, ValueError, urllib.error.URLError):
        print('error catched')

    #if the weather forecast has not changed, no alert msg will be sent
    if len(alert_msg) > 0 and previous_alert_msg == alert_msg:
        print(i, current_retrieved_datetime, 'no changes in weather forecast')
    #if there is any changes in weather       
    if len(alert_msg) > 0 and previous_alert_msg != alert_msg:    
        # login and send facebook msg 
        client = Client(FB_USERNAME,FB_PASSWORD)
        users = client.fetchAllUsers()
        friend_list=[user.uid for user in users if user.uid!="0"]
        # loop though all friends
        for id in friend_list: 
            client.send(Message(text=current_retrieved_datetime+' '+'12-hr Weather Forecast' +' '+ alert_msg +' '+link_for_click),thread_id=id, thread_type=ThreadType.USER)
            #sleep for 2 secs between each msg
            time.sleep(2) 
        #logout after sent
        client.logout()    
        time.sleep(delay_time_sec)                         
    time.sleep(update_interval_sec)
print(current_retrieved_datetime,'Run Completed')