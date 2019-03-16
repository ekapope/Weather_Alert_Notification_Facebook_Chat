# -*- coding: utf-8 -*-
"""
Define parameters to be used in the main.py script
"""
# Define % threshold for probability of rain and snow. 
# The msg will be sent out if the % chance exceed the value
RAIN_THRESHOLD = 25
SNOW_THRESHOLD = 25

# time between Accuweather request (in hour)
UPDATE_INTERVAL_HR = 1 

# delay time between msg (in hour)
DELAY_TIME_HR = 4 

# location id
# for example, https://www.accuweather.com/en/fr/lille/135564/weather-forecast/135564
# location id is 135564
LOCATION_ID = "135564" 