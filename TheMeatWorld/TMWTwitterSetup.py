import os, tweepy, tkinter

'''
read keys and tokens from 'twitterconfig.txt'
then set the keys and tokens appropriately
'''

def readConfig():
	'''
	open and read the file to "twitterSettings"
	'''
	with open(str(os.getcwd()) + "/config/TMWtwitterconfig.txt", "r") as f:  
		twitterSettings = f.readlines() 
	
	#go to that twitterSettings list and pull the key out which is between single quotes
	for i in range(0, len(twitterSettings)):
		twitterSettings[i] = twitterSettings[i].split("=")
	return twitterSettings

#set all the values for the twitter api setup and remove any possible new lines
twitterSettings = readConfig()
consumer_key = str(twitterSettings[0][1]).rstrip("\n")
consumer_secret = str(twitterSettings[1][1]).rstrip("\n")
access_token = str(twitterSettings[2][1]).rstrip("\n")
access_token_secret = str(twitterSettings[3][1]).rstrip("\n")
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)