import os

def takeScreenshot(capturePath):
	'''
	takes the screenshot, puts it in the directory and names it TweetTweet.png
	'''
	os.system("screencapture %sTweetTweet.png" %capturePath)
	
def printImage(capturePath):
	'''
	runs a command lpr that prints the file you pointed to
	'''
	os.system("lpr %sTweetTweet.png" %capturePath) 