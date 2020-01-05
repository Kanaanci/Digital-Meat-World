import sys
import os
import argparse
import pickle
import time
import markov
import twitter
import TMWScrCapPrint

parser = argparse.ArgumentParser(description='Markov chain text generator written in Python.')
parser.add_argument('-n', metavar='N', type=int, nargs=1, help='Determines length of keys in the program\'s dictionary.')
parser.add_argument('-i', metavar='I', type=int, nargs=1, help='Determines determines the length of time between tweets.')
parser.add_argument('--handles', type=str, nargs='+', help='List of twitter handles to use')
args = parser.parse_args()

#BEFORE STARTING THE BOT, THE TWTITTER ACCOUNT KEYS MUST BE SET HERE
pickle_file = 'entries.pickle'
consumer_key = 'consumer-key'
consumer_secret  = 'consumer-'
access_token_key = 'access-token'
access_token_secret = 'access-token-secret'

def setupDirectory(capturePath):
	'''
	make the directory at the capture path
	'''
	os.mkdir(capturePath) 
	
def dict_save(data, pickle_file):
	with open(pickle_file, 'a+b') as f:
		pickle.dump(data, f)

def dict_load(pickle_file):
	data = {}

	try:
		f = open(pickle_file, 'r+b')
	except FileNotFoundError:
		f = open(pickle_file, 'w+b')

	try:
		data = pickle.load(f)
	except EOFError:
		if args.handles is None:
			print("The entries file is currently empty. Perhaps provide a few Twitter handles for our bot to look at?")
			sys.exit(2)
	
	f.close()
	return data

def train(api, data, person):
	markov_prefix_length = int(args.n[0])
	total = 0
	check = 0
	oldest = None

	# Grabbing initial list of tweets
	tweets_list = api.GetUserTimeline(screen_name=person, count=1, max_id=oldest)

	while tweets_list and (oldest != check):
		try:
			tweets_list = api.GetUserTimeline(screen_name=person, 
										count=200, 
										include_rts=False,
										exclude_replies=True, 
										max_id=oldest)
		except:
			print('Something went wrong getting {person}\'s tweets. Going to next person.'.format(person=person))
			break

		total += len(tweets_list)
		check = oldest
		oldest = tweets_list[-1].id
		tweet_text = [status.full_text for status in tweets_list]

		# Pass text from status update to markov chain dictionary
		for text in tweet_text:
			for key, value in markov.parse_input(text, markov_prefix_length):

				if isinstance(key, markov.ParseLengthError):
					pass
				else:
					markov.build_dict(data, key, value)
		
		print("Processed ", total, "tweets, last tweet ID being: ", oldest)
		# Save dictionary to pickle
		dict_save(data, pickle_file)
#		print(data)


if __name__ == '__main__':
	interval = args.i[0]
	capturePath = str(os.getcwd()) + "/ImageToTweet/" #get the current working directory and add /ImageToTweet/ to it for a new folder
	startTime = time.time()
	data_table = dict_load(pickle_file)
	print(len(data_table))
	
	#does the directory exist? if not, call the function to create it
	try:
		if not os.path.exists(capturePath): 
			setupDirectory(capturePath)
	except:
		print("Something went wrong while creating the directory")
		sys.exit(2)

	# Authentication using OAuth
	try:
		twitter_api = twitter.Api(consumer_key, 
								consumer_secret, 
								access_token_key, 
								access_token_secret, 
								sleep_on_rate_limit=True,
								tweet_mode='extended')
	except:
		print("Something went wrong with authentication. Did you set your environment variables properly?")
		sys.exit(2)

	if not args.handles is None:
		for celebrity in args.handles:
			print("Fetching ", celebrity, "'s tweets...")
			train(twitter_api, data_table, celebrity)
		
	print("Generating tweets...")
	while(True):
		# Take screenshot and check the size
		TMWScrCapPrint.takeScreenshot(capturePath)
		TMWScrCapPrint.printImage(capturePath)
		
		# Generates a sentence, tweets it, then sleeps.
		text = markov.generate_sentence(data_table)

		try:
			twitter_api.PostUpdate(text.capitalize(), media='%s/TweetTweet.png' %capturePath)
		except twitter.error.TwitterError:
			pass

		print("New tweet: ", text)
		time.sleep(interval - ((time.time() - startTime) % interval))
