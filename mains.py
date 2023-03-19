import streamlit as st
import pandas as pd
import json
import snscrape.base
import snscrape.modules.twitter as sntwitter
from pymongo import MongoClient
import base64


def scraping_tweets(hashtag,start_date,end_date,tweet_limit):
    tweet_list=[]
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{hashtag} since:{start_date} until:{end_date}').get_items()):
        data=[tweet.date,tweet.id,tweet.user.username,tweet.user.verified,tweet.rawContent,tweet.lang,tweet.source,tweet.likeCount,tweet.retweetCount]
        tweet_list.append(data)
        if i==tweet_limit-1:
            break
    return tweet_list

def create_df(tweet_list):
    tweet_data = pd.DataFrame(tweet_list, columns=["Date","Id","Username","Verified","Raw Content","Language","Source","Like Count","Retweet Count"])

    return tweet_data

#GUI.py
st.image("twitter.jpg")
st.title("Scrape the Tweets")

#Get hashtag
hashtag = st.text_input("Enter the hashtag:")

#Start date
start_date = st.date_input("Select start date:", key="start_date")

#End date
end_date = st.date_input("Select end date:", key="end_date")

#Tweet limit
tweet_limit = st.number_input("Enter the number of tweet you need:", key="limit")


#Scrape tweets
if st.button("Scrape Tweets"):
    tweet = scraping_tweets(hashtag, start_date, end_date, tweet_limit)
    tweet_data = create_df(tweet)
    st.dataframe(tweet_data)
#download as csv file    
    st.write("Saving dataframe as csv")
    csv = tweet_data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv:base64,{b64}" download="tweet_data.csv">Download CSV File</a>'
    st.markdown(href,unsafe_allow_html=True)
#download as JSON
    st.write("Saving dataframe as json")
    json_string = tweet_data.to_json(indent=2)
    b64 = base64.b64encode(json_string.encode()).decode()
    href = f'<a href="data:file/json:base64,{b64}" download="tweet_data.json">Download json File</a>'
    st.markdown(href, unsafe_allow_html=True)

#upload to mongoDB
if st.button("upload to MongoDB"):
    tweet = scraping_tweets(hashtag, start_date, end_date, tweet_limit)
    tweet_data = create_df(tweet)

    client = MongoClient("mongodb://Sylvester_Berry:Berry1996@ac-igtjgce-shard-00-00.rj2uwxp.mongodb.net:27017,ac-igtjgce-shard-00-01.rj2uwxp.mongodb.net:27017,ac-igtjgce-shard-00-02.rj2uwxp.mongodb.net:27017/?ssl=true&replicaSet=atlas-2o5uoa-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = client["twitter_scrape"]
    collection = db['Leo']
    tweet_data_json = json.loads(tweet_data.to_json(orient='records'))
    collection.insert_many(tweet_data_json)
    st.success('uploaded to MongoDB')