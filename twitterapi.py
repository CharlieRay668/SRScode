import requests
import os
import json
import sqlite3
from sqlite3 import Error
import time
import random

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'

token = "AAAAAAAAAAAAAAAAAAAAAN9cJQEAAAAAVr3OCBek5GZit3lRVnl7vEtkO2k%3DE9cuhlYwNv0YM7Kn20f1lWoWuVpp90BOVpAfa5rVWYDTAhumxL"



def auth():
    return token


def create_url(ids):
    tweet_fields = "tweet.fields=text,created_at,geo,lang,author_id"
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    ids = "ids="+",".join(ids)
    # You can adjust ids to include a single Tweets.
    # Or you can add to up to 100 comma-separated IDs
    url = "https://api.twitter.com/2/tweets?{}&{}".format(ids, tweet_fields)
    return url


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def add_tweet(conn, tweet):
    """
    Create a new equity_line into the utils_data_logs_equity table
    :param conn:
    :param equity_line:
    :return: equity_line id
    """
    sql = ''' INSERT INTO tweet_db(place,tweet_id,author_id,text,geo,lang,created_at)
            VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, tweet)
    conn.commit()
    return cur.lastrowid

def divide_chunks(l, n): 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 
  

def main():
    # ids = open('2016-pres-geo.txt').readlines()
    # writer = open("2016-pres-geo-2M.txt", 'w+')
    # existing_ids = open("2016-pres-geo-1M.txt").readlines()
    # existing_ids = [i.strip() for i in existing_ids]
    # ids = [i.strip() for i in ids]
    # print(len(ids))
    # #ids = [i for i in ids if i not in existing_ids]
    # print(len(ids))
    # x = 0
    # while x < 1000000:
    #     curr_id = random.choice(ids)
    #     if curr_id not in existing_ids:
    #         writer.write(curr_id + '\n')
    #         x += 1
    #         if x%100 == 0:
    #             print(x)

    bearer_token = auth()
    ids = open('2016-pres-geo-2M.txt').readlines()
    ids = [i.strip() for i in ids]
    indexes = range(1000000)
    indexes_index = 0
    con = sqlite3.connect(r'tweetdb2.sqlite3')
    ids = ids[:1000]
    ids = list(divide_chunks(ids, 100))
    total = len(ids)
    for index, tweets in enumerate(ids):
        starttime = time.time()
        url = create_url(tweets)
        headers = create_headers(bearer_token)
        json_response = connect_to_endpoint(url, headers)
        data = json.loads(json.dumps(json_response, indent=4, sort_keys=True))
        data = data['data']
        for item in data:
            geo = None
            author_id = None
            created_at = None
            tweet_id = None
            lang = None
            text = None
            try:
                geo = item['geo']['place_id']
            except:
                geo = None
            try:
                author_id = item['author_id']
            except:
                author_id = None
            try:
                created_at = item['created_at']
            except:
                created_at = None
            try:
                tweet_id = item['id']
            except:
                tweet_id = None
            try:
                lang = item['lang']
            except:
                lang = None
            try:
                text = item['text']
            except:
                text = None
            tweet_data = [indexes[indexes_index],tweet_id, author_id, text, geo, lang, created_at]
            indexes_index += 1
            add_tweet(con, tweet_data)
            if 3 - ((time.time() - starttime) % 60.0) <= 0:
                continue
            else:
                time.sleep(3 - ((time.time() - starttime) % 60.0))
        print(index, " out of ", total)


if __name__ == "__main__":
    main()




