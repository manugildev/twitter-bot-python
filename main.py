import time
import threading
import configuration
import sys, getopt
import helpers
import twitter
from datetime import datetime
from termcolor import colored

filename = open(configuration.FILE_TARGET_USERS, "r")
targetUsers = set(filename.read().split('\n'))
followedUsers = helpers.getUsersFromFile(configuration.FILE_FOLLOWED_USERS)
followQueue = targetUsers - followedUsers

def followBot():
	try:
		print(colored("Starting Follow Bot: " + str(len(followQueue)), 'cyan', attrs=['bold']))
		time.sleep(1)
		for u in followQueue:
			if u != "" and u != "\n":
				twitter.followUser(u)
				time.sleep(int(configuration.ONE_DAY_S / configuration.FOLLOWS_PER_DAY))
		print(colored("No more users to follow!", 'red'))
	except Exception as e:
		print(e)


def unfollowBot():
	try:
		while True:
			unfollowQueue = helpers.getUsersFromFileWithDate(configuration.FILE_FOLLOWED_USERS,
			                                                 configuration.DAYS_TO_UNFOLLOW)
			print(colored("Starting UnFollow Bot: " + str(len(unfollowQueue)), 'cyan', attrs=['bold']))
			time.sleep(1)
			for u in unfollowQueue:
				if u != "" and u != "\n":
					twitter.unfollowUser(u)
					time.sleep(int(configuration.ONE_DAY_S / configuration.UNFOLLOWS_PER_DAY))
			unfollowQueue = helpers.getUsersFromFileWithDate(configuration.FILE_FOLLOWED_USERS,
			                                                 configuration.DAYS_TO_UNFOLLOW)
			if len(unfollowQueue) == 0:
				print(colored("Sleeping one hour, no elements in the unfollowing queue.", 'red'))
				time.sleep(60 * 60)

	except Exception as e:
		print(e)


def statsBot():
	print(colored("Starting Stats Bot", 'cyan', attrs=['bold']))
	time.sleep(1)
	try:
		while True:
			now = datetime.now()
			if now.hour == 0 and now.minute == 0:
				twitter.getStats(configuration.TWITTER_USERNAME)
			time.sleep(60)
	except Exception as e:
		print(e)


def bot():
	threading.Thread(target=followBot).start()
	threading.Thread(target=unfollowBot).start()
	threading.Thread(target=statsBot).start()


def main(argv):
	print(colored("======= TWITTER BOT =======", 'magenta', attrs=['bold']))
	try:
		opts, args = getopt.getopt(argv, "hf:u:d:", ["follows=", "unfollows=", "days="])
	except getopt.GetoptError:
		print('main.py -f <follows_per_day> -u <unfollows_per_days> -d <days>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('main.py -f <follows_per_day> -u <unfollows_per_days> -d <days>')
			sys.exit()
		elif opt in ("-f", "--follows"):
			configuration.FOLLOWS_PER_DAY = int(arg)
		elif opt in ("-u", "--unfollows"):
			configuration.UNFOLLOWS_PER_DAY = int(arg)
		elif opt in ("-d", "--days"):
			configuration.DAYS_TO_UNFOLLOW = int(arg)

	print(colored("------ Configuration ------", 'blue'))
	print('Follows per day: ' + str(configuration.FOLLOWS_PER_DAY))
	print('Unfollows per day: ' + str(configuration.UNFOLLOWS_PER_DAY))
	print('Days to unfollow: ' + str(configuration.DAYS_TO_UNFOLLOW))
	print(colored("---------------------------", 'blue'))

	# Create Threads that start the different modules
	bot()


if __name__ == "__main__":
	main(sys.argv[1:])
