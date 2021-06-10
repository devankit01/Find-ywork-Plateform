# import geocoder
# g = geocoder.ip('me')
# print(g)

# # import module
# from geopy.geocoders import Nominatim
# # initialize Nominatim API
# geolocator = Nominatim(user_agent="geoapiExercises")
# # initialize Nominatim API
# geolocator = Nominatim(user_agent="geoapiExercises")
# place = g[0]
# location = geolocator.geocode(place)
# print(location)

# # importing the module
# import pywhatkit

# # using Exception Handling to avoid
# # unprecedented errors
# try:

#     # sending message to reciever
#     # using pywhatkit
#         pywhatkit.sendwhatmsg("+919149562195",
#                             "Hello from GeeksforGeeks",
#                             22, 28)
#         print("Successfully Sent!")

# except:

#     # handling exception
#     # and printing error message
#     print("An Unexpected Error!")


# import way2sms
# # your login credentials
# sms = way2sms.SMS("+918529519096", "password")
# sms.send("+919140562195", "Hi, this package is awesome! Lets me send free messages")
# sms.logout()


# from twilio.rest import Client
# i = 1
# account_sid = 'ACdc2fb4e2b92b67953f39257b118a7487'
# auth_token = '2cec0390e9bf428a42134d5800f9655b'
# client = Client(account_sid, auth_token)
# content = "Hello !" + str(i)
# message = client.messages.create(body=content,from_='+13362838190',to='+919140562195')
# print(message.sid)



# # 
# import os
# from twilio.rest import Client
# from twilio.http.http_client import TwilioHttpClient

# proxy_client = TwilioHttpClient()
# proxy_client.session.proxies = {'https': os.environ['https_proxy']}

# i = 1
# account_sid = 'ACdc2fb4e2b92b67953f39257b118a7487'
# auth_token = '2cec0390e9bf428a42134d5800f9655b'
# client = Client(account_sid, auth_token, http_client=proxy_client)
# content = "Hello !" + str(i)
# message = client.messages.create(body=content,from_='+13362838190',to='+919140562195')
# print(message.sid)
