#!/usr/bin/python3
import tweepy
import json
import sys
sys.path.insert(0, "/home/haoyangw/Documents/tweepy/")
import privateKey


# auth the Key and secret
auth = tweepy.OAuthHandler(privateKey.consumer_key, privateKey.consumer_secret)
auth.set_access_token(privateKey.access_token, privateKey.access_token_secret)

# get handler
api = tweepy.API(auth)

#tweets = api.user_timeline('BotMeal')
tweets = tweepy.Cursor(api.search, q='#朴素一餐').items(5)

for tweet in tweets:
    print(tweet.author.name + ':')
    print("time:" + str(tweet.created_at.year) + "/" + str(tweet.created_at.month) + '/' + str(tweet.created_at.day) +
          ' ' + str(tweet.created_at.hour) + ':' + str(tweet.created_at.minute) + ':' + str(tweet.created_at.second))
    print("text:" + tweet.text)
    if hasattr(tweet,'extended_entities') :
        media = tweet.extended_entities['media']
        for i in range(len(media)):
                print("    " + str(media[i]['type']) + str(i) + ":")
                print("        id: " + str(media[i]['id']))
                print("        https_url: " + str(media[i]['media_url_https']))
    print("===============================================")
