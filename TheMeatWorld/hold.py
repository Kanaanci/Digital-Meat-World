		import os, sys, signal, time, datetime, TMWTwitterSetup
		from pathlib import Path

		def signal_handler(signal, frame):
			'''
			we have an infinite loop in main so we need a way to exit gracefully
			this is it, signals
			'''
			print("\nProgram exiting gracefully")
			sys.exit(0)

		signal.signal(signal.SIGINT, signal_handler)
		def setupDirectory(capturePath):
			'''
			make the directory at the capture path
			'''
			os.mkdir(capturePath) 

		def readConfig():
			'''
			read the configuration file
			this file allows the user to change different settings without
			actually altering the code
			'''
			with open(str(os.getcwd()) + "/config/TMWbotconfig.txt", "r") as f:
				botSettings = f.readlines()
					
			#go to that botSettings list and pull the key out which is between single quotes
			for i in range(0, len(botSettings)):
				botSettings[i] = botSettings[i].split("=")
				
			return botSettings
				
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
			
		def postToTwitter(capturePath):
			'''
			generate a timestamp to post as the message to the tweet
			create a variable for file size in mb as the twitter api limits photos to be less than 3mb
			check if image is less than 3mb
			'''
			fileSizeMb = os.path.getsize('%s/TweetTweet.png' %capturePath) / 1024
			timeStamp = datetime.datetime.now() 

			#if the image is less than 3mb then post it
			if fileSizeMb < 3072:
				TMWTwitterSetup.api.update_with_media('%s/TweetTweet.png' %capturePath, status=timeStamp) #post the given file with a status on twitter
			
		def main():
			capturePath = str(os.getcwd()) + "/ImageToTweet/" #get the current working directory and add /ImageToTweet/ to it for a new folder
			startTime = time.time()
			botSettings = readConfig() #get the list of settings for the bot from readConfig()
			interval = float(botSettings[0][1]) #interval is at [0][1]
			
		#	message = str(botSettings[1][1]).rstrip("\n") #may be removed. Not sure what logan will want with the status message for twitter
			
			#does the directory exist? if not, call the function to create it
			if not os.path.exists(capturePath): 
				setupDirectory(capturePath)

			#run this every x amount of seconds
			while True:
				print("tick")
				takeScreenshot(capturePath)
		#		postToTwitter(capturePath)
		#		printImage(capturePath)
				time.sleep(interval - ((time.time() - startTime) % interval))
				
					
		if __name__ == "__main__":
			main()
