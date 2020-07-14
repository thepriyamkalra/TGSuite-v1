#!/usr/bin/env python3
#this code is written by @sauravdharwadkar
#the purpose of this code to locally generate google's oauthclient json file to use in any where it needed 
#do not share oauth file to public it content authentication data 


try:
	import oauth2client
except Exception as e:
	import pip
	pip.main(['install', "oauth2client"])

from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
print("\n"*1000) # easy way to clear console
print("Follow the tutorial and get the CLIENT_ID , CLIENT_SECRET from google :")
print("\033[35m","https://telegra.ph/The-TG-Bot-Drive-Setup-Tutorial-07-04","\033[0m")
print("\n\nEnter / paste Follow info : \n")
scope = "https://www.googleapis.com/auth/drive.file"
uri = "urn:ietf:wg:oauth:2.0:oob"
CLIENT_ID = input("paste CLIENT_ID :")
CLIENT_SECRET = input ("paste CLIENT_SECRET :")
oasF = OAuth2WebServerFlow(CLIENT_ID,CLIENT_SECRET,scope,uri)
auth_uri = oasF.step1_get_authorize_url()

print("open url in brouser and give permission with your Drive login aka google login :\n ",auth_uri)
try:
	credentials = oasF.step2_exchange(input("\npaste code given by google : "))
except Exception as e:
	print("\nYou enter Wrong info / Code")
	exit(0)

Local_File = Storage("authData.txt")
Local_File.put(credentials)
print ("put following data to heroku ENV variable DRIVE_AUTH_TOKEN_DATA: \n\n")
with open('authData.txt', 'r') as f:
    print(f.read())
print("\n\n")
