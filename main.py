import tweepy
import time
import threading
import configuration
import sys, getopt
from datetime import datetime
from termcolor import colored

API_KEY = configuration.keys['API_KEY']
API_SECRET = configuration.keys['API_SECRET']
ACCESS_TOKEN = configuration.keys['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = configuration.keys['ACCESS_TOKEN_SECRET']
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

filename = open("files/targetUsers.txt", "r")
targetUsers = set(filename.read().split('\n'))


def updateStatus(msg):
    api.update_status(status=msg)


def followUser(user):
    try:
        api.create_friendship(screen_name=user)
        appendToFile(configuration.FILE_FOLLOWED_USERS, getDate() + ", " + user)
        print(colored("User followed: " + user, 'green'))
    except Exception as e:
        print(colored(e, 'red'))


def unfollowUser(user):
    try:
        api.destroy_friendship(screen_name=user)
        appendToFile(configuration.FILE_UNFOLLOWED_USERS, getDate() + ", " + user)
        print(colored("User unfollowed: " + user, 'red'))
    except Exception as e:
        print(colored(e, 'red'))


def getStats(user):
    result = api.get_user(screen_name=user)
    following = str(result.friends_count)
    followers = str(result.followers_count)
    tweets = str(result.statuses_count)
    favourites = str(result.favourites_count)
    print(colored("===========================", 'cyan'))
    print("STATS of @" + user)
    print("---------------------------")
    print("Time: " + getDate())
    print("Tweets: " + tweets)
    print("Following: " + following)
    print("Followers: " + followers)
    print("Favourites: " + favourites)
    print(colored("===========================", 'cyan'))
    appendToFile(configuration.FILE_STATS,
                 "{}:{}:{}:{}:{}".format(getCurrentMillis(), tweets, following, followers, favourites))


def appendToFile(filename, msg):
    f = open(filename, 'a')
    f.write(msg + "\n")
    f.close()


def getCurrentMillis():
    return int(round(time.time() * 1000))


def getDate():
    localtime = time.localtime()
    return time.strftime("%d/%m/%y %H:%M:%S", localtime)


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


def followBot():
    try:
        print(colored("Starting Follow Bot: " + str(len(followQueue)), 'cyan'))
        for u in followQueue:
            if u != "" and u != "\n":
                followUser(u)
                time.sleep(int(configuration.ONE_DAY_S / configuration.FOLLOWS_PER_DAY))
        print(colored("No more users to follow!", 'red'))
    except Exception as e:
        print(e)


def unfollowBot():
    try:
        while True:
            unfollowQueue = getUsersFromFileWithDate(configuration.FILE_FOLLOWED_USERS, configuration.DAYS_TO_UNFOLLOW)

            print(colored("Starting UnFollow Bot: " + str(len(unfollowQueue)), 'cyan'))
            for u in unfollowQueue:
                if u != "" and u != "\n":
                    unfollowUser(u)
                    time.sleep(int(configuration.ONE_DAY_S / configuration.UNFOLLOWS_PER_DAY))

            unfollowQueue = getUsersFromFileWithDate(configuration.FILE_FOLLOWED_USERS, configuration.DAYS_TO_UNFOLLOW)

            if len(unfollowQueue) == 0:
                print(colored("Sleeping one hour, no elements in the unfollowing queue.", 'red'))
                time.sleep(60 * 60)

    except Exception as e:
        print(e)


def statsBot():
    print(colored("Starting Stats Bot", 'cyan'))
    try:
        while True:
            now = datetime.now()
            if now.hour == 0 and now.minute == 0:
                getStats(configuration.TWITTER_USERNAME)
            time.sleep(60)
    except Exception as e:
        print(e)


followedUsers = getUsersFromFile(configuration.FILE_FOLLOWED_USERS)
unfollowQueue = getUsersFromFileWithDate(configuration.FILE_FOLLOWED_USERS, configuration.DAYS_TO_UNFOLLOW)
followQueue = targetUsers - followedUsers


def main(argv):
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
            configuration.FOLLOWS_PER_DAY = arg
        elif opt in ("-u", "--unfollows"):
            configuration.UNFOLLOWS_PER_DAY = arg
        elif opt in ("-d", "--days"):
            configuration.DAYS_TO_UNFOLLOW = arg

    print(colored("====== Configuration ======", 'magenta'))
    print('Follows per day: ' + str(configuration.FOLLOWS_PER_DAY))
    print('Unfollows per day: ' + str(configuration.UNFOLLOWS_PER_DAY))
    print('Days to unfollow: ' + str(configuration.DAYS_TO_UNFOLLOW))
    print(colored("===========================", 'magenta'))

    # Create Threads that start the different modules
    threading.Thread(target=followBot).start()
    threading.Thread(target=unfollowBot).start()
    threading.Thread(target=statsBot).start()


if __name__ == "__main__":
    main(sys.argv[1:])
