import tweepy
import csv
import pandas as pd
import json

#Tweets 14 days backwards for specified hashtag

with open('twitter_credentials.json') as cred_data:
    info = json.load(cred_data)
consumer_key = info['CONSUMER_KEY']
consumer_secret = info['CONSUMER_SECRET']
access_key = info['ACCESS_KEY']
access_secret = info['ACCESS_SECRET']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)
#####United Airlines
# Open/Create a file to append data
csvFile = open('NAME OF FILE', 'w', encoding='utf-8')
#Use csv Writer
csvWriter = csv.writer(csvFile, delimiter=',',quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

for tweet in tweepy.Cursor(api.search,q="HASHTAG",count=200, tweet_mode='extended', #Replace hashtag with wanted hashtag
                           since="2017-04-03").items():
    print (tweet.id_str, tweet.created_at, tweet.full_text, tweet.favorite_count, tweet.retweet_count, tweet.user.location)
    csvWriter.writerow([tweet.id_str, tweet.created_at, tweet.full_text, tweet.favorite_count, tweet.retweet_count, tweet.user.location])