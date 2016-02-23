import configuration
import time
from twilio.rest import TwilioRestClient
from datetime import datetime


def appendToFile(filename, msg):
	f = open(filename, 'a')
	f.write(msg + "\n")
	f.close()


def getCurrentMillis():
	return int(round(time.time() * 1000))


def getDate():
	localtime = time.localtime()
	return time.strftime("%d/%m/%y %H:%M:%S", localtime)


def getTime():
	localtime = time.localtime()
	return time.strftime("%H:%M:%S", localtime)


def toUnixTime(timestamp):
	epoch = datetime.utcfromtimestamp(0)  # start of epoch time
	my_time = timestamp
	delta = my_time - epoch
	return delta.total_seconds() * 1000.0


def getUsersFromFile(filename):
	lines = open(filename, 'r').read().split('\n')
	result = []
	for line in lines:
		if (line != "" and line != "\n"):  # With this we remove all black lines and stuff
			result.append(line[line.index(",") + 2:])
	return set(result)


def getUsersFromFileWithDate(filename, days):
	lines = open(filename, 'r').read().split('\n')
	result = []
	for line in lines:
		if (line != "" and line != "\n"):  # With this we remove all black lines and stuff
			time = datetime.strptime(line[:line.index(",")], "%d/%m/%y %H:%M:%S")
			now = datetime.now()
			if int(toUnixTime(now) - toUnixTime(time)) > days * configuration.ONE_DAY_MS:
				result.append(line[line.index(",") + 2:])
	return set(result) - getUsersFromFile(configuration.FILE_UNFOLLOWED_USERS)


def sendMessage(tweets, following, followers, favourites):
	try:
		ACCOUNT_SID = configuration.TWILIO_ACCOUNT_SID
		AUTH_TOKEN = configuration.TWILIO_AUTH_TOKEN
		client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
		msg = "=\nTweets: " + str(tweets) + "\nFollowing: " + str(following) + "\nFollowers: " + str(followers)
		client.messages.create(
			to=configuration.TWILIO_TO_PHONE,
			from_=configuration.TWILIO_FROM_PHONE,
			body=msg)
	except Exception as a:
		print(a)
