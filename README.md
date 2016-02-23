# Twitter Bot
![image](http://i.imgur.com/mCjs953.png =400x)
## Overview
This bot was originally made to run on a **RaspberryPi**, without any user interaction, you just start it and it should automatically follow and unfollow X number of users per day.

It works using the twitter api and the module **tweepy**.

Every day at 00:00AM it should save all the important stats of your twitter account to the file at *files/stats.txt* with the following format:	

	time:statuses_count:friends_count:followers_count:favourites_count
		
Time is in Milliseconds format, if you want to now the date you can use <http://currentmillis.com/>.
## Requirements

You need to have installed 2 Python modules, tweepy and termcolor. To install those, use the following commands (for python 3+ use *pip3* instead of *pip*):
	
	pip install tweetpy 
	pip install termcolor
	
You will also need to have the file structure has I have it, but you can always change the paths in *configuration.py*.

	files/
		stats.txt				# Stores the stats of your twitter account
		targetUsers.txt			# Stores the users you are going to follow
		followedUsers.txt		# Stores the users that have been followed
		unfollowedUsers.txt		# Stores the users that have been unfollowed		

## Use
1. Modify the file configuration.py filling the places where there are some **"=================="** with your keys and username


		keys = {"API_KEY"				: "=====================",
        		"API_SECRET"			: "=====================",
        		"ACCESS_TOKEN"			: "=====================",
        		"ACCESS_TOKEN_SECRET"	: "====================="}
        		
        TWITTER_USERNAME 				= "==========="                        
2. Open a terminal on your pc and run:

		python main.py -f 1000 -u 1000 -d 2
	
	Where the available parameteres are:

	* -f \<follows_per_day\> - Number of follows per day
	* -u \<unfollows_per_days\> - Number of unfollows per day
	* -d \<days\> - days to wait to unfollow a user


## Credits

If you have any problem using it, contact me by twitter **[@gikdew](https://twitter.com/gikdew)**
