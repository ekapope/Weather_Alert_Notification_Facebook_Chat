# Weather Alert Notification Script using Facebook Chat [weather data from AccuWeather API]

This is another version of DIY weather alert system. The first version is [here](https://github.com/ekapope/WeatherAlertNotification) using Gmail and Twitter API.


## Why do you need this?

80% of smartphone users check their phone within 15 minutes after waking up in the morning for social media, emails and weather. Won't it be wonderful if you have one less thing to worry in the morning?

What if you have a customized weather alert which will automatically send you a short message ONLY when there is a chance of rain above your pre-defined threshold with fully customizable functions. 

Since you are checking emails and social media anyway, do not waste your time checking the weather on the separated app. It is now live on your facebook msg box!

![FB_Chat_Screenshot](https://github.com/ekapope/Weather_Alert_Notification_Facebook_Chat/blob/master/Capture_Facebook_Chat_msg.PNG)


### There are 3 files in the scripts folder:
- keys.py : put your facebook email, password, and accuweather API key here
- main.py : this is the main script, it will call the keys.py and params.py
- params.py : modify the threshold and location here


### Here are requirements for the setup:

- Python 3.6 with pandas and fbchat packages installed
- [AccuWeather developer account](https://developer.accuweather.com/packages)
- [Facebook chat setup](https://github.com/carpedm20/fbchat)

Please give it a try, enjoy and let me know your feedback! 

#### [A complete guide with explaination is published on Medium](https://medium.freecodecamp.org/how-to-get-facebook-messenger-to-notify-you-about-the-weather-8b5e87a64540).

