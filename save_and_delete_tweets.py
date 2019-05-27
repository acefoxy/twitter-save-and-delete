
import tweepy #https://github.com/tweepy/tweepy
import csv
from datetime import datetime, timedelta


#add user with @
user = '@AndreasNL'

#days to keep
days_to_keep = 14

#Twitter API credentials
consumer_key=''
consumer_secret=''
access_key=''
access_secret=''




date = datetime.utcnow().date()



def get_all_tweets(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method

    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    #initialize a list to hold all the tweepy Tweets
    alltweets = []

    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)

    #save most recent tweets
    alltweets.extend(new_tweets)

    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print ("getting tweets before %s" % (oldest))

        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

        #save most recent tweets
        alltweets.extend(new_tweets)

        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print ("...%s tweets downloaded so far" % (len(alltweets)))

    #transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]

    #write the csv
    with open('%s_tweets.csv' % date, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text"])
        writer.writerows(outtweets)

    pass


def delete_tweets(days_to_keep):
	print(days_to_keep)
	#Twitter only allows access to a users most recent 3240 tweets with this method
	cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)

	timeline = tweepy.Cursor(api.user_timeline).items()
	deletion_count = 0
	ignored_count = 0


	for tweet in timeline:
		if tweet.created_at < cutoff_date:


			api.destroy_status(tweet.id)
			deletion_count += 1
			print(deletion_count)


	print(deletion_count)




get_all_tweets(user)
delete_tweets(days_to_keep)
