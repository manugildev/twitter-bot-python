import tweepy
import configuration
from termcolor import colored
from helpers import getDate, getCurrentMillis, appendToFile, getTime

API_KEY = configuration.keys['API_KEY']
API_SECRET = configuration.keys['API_SECRET']
ACCESS_TOKEN = configuration.keys['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = configuration.keys['ACCESS_TOKEN_SECRET']
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def updateStatus(msg):
    api.update_status(status=msg)


def followUser(user):
    try:
        api.create_friendship(screen_name=user)
        appendToFile(configuration.FILE_FOLLOWED_USERS, getDate() + ", " + user)
        print(colored(getTime() + " User followed: " + user, 'green'))
    except Exception as e:
        print(colored(e, 'red'))


def unfollowUser(user):
    try:
        api.destroy_friendship(screen_name=user)
        appendToFile(configuration.FILE_UNFOLLOWED_USERS, getDate() + ", " + user)
        print(colored(getTime() + " User unfollowed: " + user, 'red'))
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
