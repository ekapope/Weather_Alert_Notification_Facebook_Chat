# -*- coding: utf-8 -*-
"""
This is a customize weather forcast alert (12 hours forecast from AccuWeather API)
It will send an msg alert based on user setting (func_get_weather), for loop

input: starts from line 20, 80
output: facebook msg

"""

import urllib
import urllib.parse
import json
import time
import requests
import pandas as pd

####################################################################################################
# Define % cutoff for probability of rain and snow.
# The msg will be sent out if the % chance exceed the value
rain_prob_cutoff = 10
snow_prob_cutoff = 10
Checking_interval_hr = 1 # time between Accuweather request in hour
DelayTime_hr = 4 # delay time between msg (if sent)
####################################################################################################
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
    json_df['% Rain'] = json_df['RainProbability'] 
    json_df['% Snow'] = json_df['SnowProbability'] 
    json_df[['Date','Time']] = json_df['DateTime'].str.split('T', expand=True)
    # trim the time to hh:mm format, change to str
    json_df[['Time']] = json_df['Time'].str.split('+', expand=True)[0].astype(str).str[:5]
       
    current_retrieved_datetime = str(json_df['Date'][0])+' '+str(json_df['Time'][0])
    
    check_rain=""
    check_snow=""
    # check % rain column
    for i in range(0, len(json_df)):
        if json_df['% Rain'][i] > rain_prob_cutoff:
            check_rain= ", there is "+str(json_df['% Rain'][i])+"% chance of Rain @ "+str(json_df['Time'][i])
            break
    # check % snow column           
    for i in range(0, len(json_df)):
        if json_df['% Snow'][i] > snow_prob_cutoff:
            check_snow= ", there is "+str(json_df['% Snow'][i])+"% chance of Snow @ "+str(json_df['Time'][i])
            break
        else: "There will be no rain nor snow, have a good day!"
        
    alert_msg = check_rain +" "+check_snow
    link_for_click = json_df['MobileLink'][0]
    
    return(current_retrieved_datetime,alert_msg,link_for_click)
    
####################################################################################################
# Facebook Setup
# credited: https://python3.wannaphong.com/2019/01/facebook-python.html?fbclid=IwAR0EODLS6ZUbLZeCtT2-T9SYIRKc299dFzaIG-QGqPJ2LVKZ6BGu9BCOVa0&m=1
# https://github.com/carpedm20/fbchat/blob/master/examples/basic_usage.py
import sys
from fbchat import Client
from fbchat.models import *
fb_username= "Your Facebook usersname" # Your Facebook usersname
fb_password= "Your Facebook password" # Your Facebook password
client = Client(fb_username,fb_password)
users = client.fetchAllUsers()
listuser=[user.uid for user in users if user.uid!="0"] # retrieve all friends uid, save in listuser
#client.logout() # logout
####################################################################################################
# Get Weather
location = "Your desired location" # location id (the last number in accuweather url)
myapikey= "Your Accuweather API key"
url_page = "http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/"+str(location)+"?apikey="+myapikey+"&details=true&metric=true"
####################################################################################################
# Setup # of loops and sleep delay time
num_repeat = 999 # number of loops to repeat
previous_alert_msg = "" # initialize alert msg
Sleeptime = 60*60*Checking_interval_hr # accuweather request sleep time interval in seconds (60*60 = 1 hr)
delay_time = 60*60*DelayTime_hr # delay time if execute (sent)
####################################################################################################
# Execute functions, retrieve data and send facebook msg
for i in range(num_repeat):

    time_old = ''
    try:
        current_retrieved_datetime,alert_msg,link_for_click = func_get_weather(url_page)
    except (RuntimeError, TypeError, NameError, ValueError, urllib.error.URLError):
        print('error catched')

# check if there is any changes in weather
    if len(alert_msg) > 0 and previous_alert_msg == alert_msg:
        print(i, current_retrieved_datetime, 'no changes in weather forecast')
        
    if len(alert_msg) > 0 and previous_alert_msg != alert_msg:
####### Send facebook msg        
        client = Client(fb_username,fb_password) # login
        users = client.fetchAllUsers()
        for id in listuser: # loop for all uid in the list
            client.send(Message(text=current_retrieved_datetime+' '+'12-hr Weather Forecast' +' '+ alert_msg +' '+link_for_click),thread_id=id, thread_type=ThreadType.USER)
            time.sleep(2) # sleep for 2 secs between each msg
        client.logout() # logout after sent   
        time.sleep(delay_time)                         
    time.sleep(Sleeptime)
print(current_retrieved_datetime,'Run Completed')