import requests
from requests_oauthlib import OAuth1
import os

# Replace with your Twitter API credentials
API_KEY = os.getenv('API_KEY')
API_SECRET_KEY = os.getenv('API_SECRET_KEY')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')  # You can set this as an environment variable for security
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

# Create OAuth1 object for authentication
auth = OAuth1(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

def reply_to_tweet(tweet_id, username, reply_text):
    # Construct the reply text including the mention
    tweet_text = f"@{username} {reply_text}"

    # url = "https://api.twitter.com/1.1/statuses/update.json"
    url = "https://api.twitter.com/2/tweets"
    params = {
        "status": tweet_text,
        "in_reply_to_status_id": tweet_id,
        "auto_populate_reply_metadata": True  # Automatically add other users mentioned in the original tweet
    }

    response = requests.post(url, auth=auth, params=params)

    if response.status_code == 200:
        print("Reply posted successfully.")
    else:
        print(f"Failed to post reply: {response.status_code}")
        print(response.text)

# Example usage
original_tweet_id = '1830714753452515419'  # Replace with the tweet ID you want to reply to
username_to_reply = 'gcc_x_sa'  # Replace with the username of the person you're replying to
reply_text = "We are monitoring the progress. Thanks for updating."
reply_to_tweet(original_tweet_id, username_to_reply, reply_text)

