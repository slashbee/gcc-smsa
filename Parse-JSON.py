import json

# Path to your JSON file
file_path = 'data1.json'

# Open the JSON file and load its contents
with open(file_path, 'r') as file:
    data = json.load(file)

# Access and print specific elements
print("Start Date:", data['analysis_start_date'])
print("End Date:", data['analysis_end_date'])
print("Platform:", data['platform'])
print("Total Posts:", data['total_posts_analyzed'])
print("Positive Posts:", data['sentiment_summary']['positive'][0],"\t\tPercentage: ",data['sentiment_summary']['positive'][1])
print("Neutral Posts:", data['sentiment_summary']['neutral'][0],"\t\tPercentage: ",data['sentiment_summary']['neutral'][1])
print("Negative Posts:", data['sentiment_summary']['negative'][0],"\tPercentage: ",data['sentiment_summary']['negative'][1])

# If you want to print the entire JSON data
#print("\nFull JSON Data:")
#print(json.dumps(data, indent=4))

