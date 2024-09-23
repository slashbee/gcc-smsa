import requests
import os

### Function to convert user ID to username

def get_username_from_userid(user_id):
    url = f"https://api.twitter.com/2/users/{user_id}"
    
    # Set up the request headers with your bearer token
    headers = {
        'Authorization': f'Bearer {bearer_token}',
    }
    
    # Make the request to the API
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        user_data = response.json()
        return user_data['data']['username']
    else:
        print(f"Failed to retrieve user: {response.status_code}")
        print(response.text)
        return None

### End function

# Set your X API keys and tokens
bearer_token = os.getenv('BEARER_TOKEN')  # You can set this as an environment variable for security

# Set up the request headers with your bearer token
headers = {
    'Authorization': f'Bearer {bearer_token}',
}

# Endpoint URL for retrieving recent tweets mentioning the authenticated user
url = 'https://api.twitter.com/2/tweets/search/recent'


# Query parameter to search for tweets mentioning the authenticated user
query = '@ChennaiCorp'  # Replace with your actual username

# Set up query parameters
params = {
    'query': query,
    'tweet.fields': 'created_at,text,author_id,id,lang,conversation_id,attachments',
    'max_results': 100  # Number of tweets to retrieve, can be between 10 to 100
}

# Make the request to the API
response = requests.get(url, headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:
    tweets = response.json()
    for tweet in tweets['data']:
        print(f"Tweet Poster : ", get_username_from_userid(tweet['author_id']))
        print(f"Tweet Language: ",{tweet['lang']})
        print(f"Tweet ID: ",{tweet['id']})
        print(f"Tweet at: ",{tweet['created_at']})
        print(f"Tweet:,{tweet['text']}")
else:
    print(f"Failed to retrieve tweets: {response.status_code}")
    print(response.text)

