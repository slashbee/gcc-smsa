import os
import boto3

# Initialize AWS Comprehend client
comprehend = boto3.client('comprehend')

###################################################
# Function to the translate from Tamil to English #
###################################################

def translate_text(text, source_language_code, target_language_code):
        # Initialize a boto3 client for AWS Translate
        """Initialize a boto3 client for AWS Translate
        This will be invoked when we run into Tamil Tweet
        But, this can be used to translate from/to any language(s)
	"""
        translate = boto3.client(service_name='translate', region_name='ap-southeast-1', use_ssl=True)        
        # Use the translate_text method
        result = translate.translate_text(
            Text=text,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code
        )       
        #print(result['TranslatedText'])    
        return result['TranslatedText']

############# Function ends here ############


def analyze_sentiment(text):
    # Call AWS Comprehend to detect sentiment
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    print(response['SentimentScore']['Negative'])
    if response['SentimentScore']['Negative'] > 0.10:
       print(text)
       return 'NEGATIVE'
    else:
       return response['Sentiment']

def analyze_file_sentiment(file_path):
    with open(file_path, 'r') as file:
        flag = 0
        for line_number, line in enumerate(file, start=1):
            line = line.strip()  # Remove leading/trailing whitespace
            if line:  # Skip empty lines
              if line.startswith('Tweet Language:'):
                #print(get_tweet_language(line))
                if get_tweet_language(line) == 'ta':
                   flag = 1
                   #print("*****")
                   #print(line)
              elif line.startswith('Tweet:'):
                if flag == 1:
                    tline = translate_text(line,'ta','en')
                    #print(tline)
                    sentiment = analyze_sentiment(tline)
                    flag = 0
                else:
                    #print(line)
                    sentiment = analyze_sentiment(line)
                    #print(f"Line {line_number}: {line}")
                    #print(f"Sentiment: {sentiment}\n")
                    #print(sentiment)
                return sentiment

def get_tweet_language(text):
        idx1 = text.index('{')
        idx2 = text.index('}')
 
        res = ''
        # getting elements in between
        for idx in range(idx1 + 2, idx2-1):
            res = res + text[idx]
        #print(res)
        return res

def check_lines_starting_with_keyword(file_path, keyword):
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()  # Remove leading/trailing whitespace
            if line.startswith(keyword):
                #print(f"Line {line_number} starts with '{keyword}': {line}")
                return line

folder_path = './tweets'
keyword = 'Tweet:'
for root, dirs, files in os.walk(folder_path):
        for filename in files:
            # Construct the full local path
            local_path = os.path.join(root, filename)
            print(analyze_file_sentiment(local_path))
            
