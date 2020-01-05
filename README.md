Digital Meat World was created for a Kent State University art student.

This program is a Twitter bot that uses a Markov style chain to generate tweets from a dictionary of words taken from a list of Twitter users.
After generating a Tweet, it takes a screenshot of the users desktop and posts the image and tweet to Twitter as well as printing the image at the computers default printer.
To use this program, a Twitter Developer account must be used. The API keys must be placed in the "TheMeatWorld.py" file.

<u>Commandline Arguments</u>
-n: Determinds the length of keys in the program's dictionary
-i: Determines the length of time between tweets
--handles: the list of Twitter users to pull Tweets from

Example command:
<b>python3 TheMeatWorld.py -n 20 -i 120 --handles @SadSocrates @philosophytweet @existentialcoms</b>
