#!/usr/bin/env python
# encoding: utf-8
#Collects tweets for specified account. You need credentials from Twitter.
# Put credentials in json file
import os, sys
import tweepy  # https://github.com/tweepy/tweepy
import csv
import json

with open('INPUT CREDENTIAL FILE') as cred_data:
    info = json.load(cred_data)
consumer_key = info['CONSUMER_KEY']
consumer_secret = info['CONSUMER_SECRET']
access_key = info['ACCESS_KEY']
access_secret = info['ACCESS_SECRET']


def get_all_tweets(screen_name):
    # Twitter only allows access to a users most recent 3240 tweets with this method

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)


    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200, tweet_mode='extended')

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("getting tweets before {}".format(oldest))

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest, tweet_mode='extended')

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print("...{} tweets downloaded so far".format(len(alltweets)))

    # transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, tweet.created_at, tweet.full_text, tweet.favorite_count, tweet.retweet_count, tweet.lang] for tweet in alltweets]

    # write the csv
    with open('{}_tweets.csv'.format(screen_name), 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',',quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        writer.writerow(["id","created_at","full_text","favorite_count", "retweet_count","lang"])
        writer.writerows(outtweets)
        print('{}_tweets.csv was successfully created.'.format(screen_name))
    pass


if __name__ == '__main__':
    # pass in the username of the account you want to download
    get_all_tweets("PUT NAME HERE")