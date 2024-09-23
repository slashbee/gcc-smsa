import requests
from requests_oauthlib import OAuth1
import os

# Set your X API keys and tokens
bearer_token = os.getenv('BEARER_TOKEN')  # You can set this as an environment variable for security
API_KEY = os.getenv('API_KEY')
API_SECRET_KEY = os.getenv('API_SECRET_KEY')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

auth = OAuth1(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

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

### Function to send DM to user ID
def send_direct_message(user_id, message_text):

    url = "https://api.twitter.com/1.1/direct_messages/events/new.json"
    message_data = { 
        "event": {
            "type": "message_create",
            "message_create": {
                "target": {
                    "recipient_id": user_id
                },  
                "message_data": {
                    "text": message_text
                }   
            }   
        }   
    }   
    response = requests.post(url, auth=auth, json=message_data)

    # Check if the request was successful
    if response.status_code == 200:
        print(f"Message sent successfully to user ID {user_id}.")
    else:
        print(f"Failed to send message: {response.status_code}")
        print(response.text)
### End function



print(get_username_from_userid('1815656230125445120'))
send_direct_message('1815656230125445120', 'Hello World!')
