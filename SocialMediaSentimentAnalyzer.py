import glob
import os
import pandas as pd
import boto3
from langdetect import detect, DetectorFactory
from PIL import Image
import pytesseract

# We do not impose limits on the # of columns
pd.set_option("display.max_columns", None)

# Ensure consistent results
DetectorFactory.seed = 0

#############################################
# Function to detect the grievance language #
#############################################

def detect_language(text):
	try:
		language = detect(text)
		return language
	except Exception as e:
		return str(e)

############# Function ends here ############

###################################################
# Function to the translate from Tamil to English #
###################################################

def translate_text(text, source_language_code, target_language_code):
	# Initialize a boto3 client for AWS Translate
	translate = boto3.client(service_name='translate', region_name='ap-southeast-1', use_ssl=True)
	
	# Use the translate_text method
	result = translate.translate_text(
	    Text=text,
	    SourceLanguageCode=source_language_code,
	    TargetLanguageCode=target_language_code
	)
	
	return result['TranslatedText']

############# Function ends here ############

#########################################################
# Function to allow the user to choose from two options #
# One to process the text corpus from an Excel file     #
# The other is to extract the text from SM screenshots  #
#########################################################

def get_user_choice():
    while True:
        print("\n\n" + "Please choose one of the following options:" + "\n\n")
        print("1. Process Social media data that is collected and gathered into an Excel File"+"\n")
        print("2. Extract and Process text in the screenshots of Social Media post from public"+"\n")
        print("3. Start the automated Social media to scrub and process the grievances from the GCC feed"+"\n")
        
        choice = input("Enter 1 or 2 or 3: ")
        
        if choice == '1':
            return 1
        elif choice == '2':
            return 2
        elif choice == '3':
            return 3
        else:
            print("Invalid input. Please enter 1 or 2.")

############# Function ends here ############


#########################################################
# Function to allow the user to choose from two options #
# One to process the text corpus from an Excel file     #
# The other is to extract the text from SM screenshots  #
#########################################################
def process_image_files(folder_path):
    # Use glob to find all image files in the folder
    image_files = glob.glob(os.path.join(folder_path, '*.jpg')) + glob.glob(os.path.join(folder_path, '*.jpeg')) + glob.glob(os.path.join(folder_path, '*.png')) + glob.glob(os.path.join(folder_path, '*.JPG')) + glob.glob(os.path.join(folder_path, '*.JPEG')) + glob.glob(os.path.join(folder_path, '*.PNG'))
    
    # Print the names of the JPEG files
    i = 0
    for file in image_files:
        i = i + 1
        print(" Processing ./images/" + os.path.basename(file) + " ...\n")
        image = Image.open("./images/" + os.path.basename(file))
        text = pytesseract.image_to_string(image)
        # print(text)
        output_file_name = f'./grievances_i/file_{i}.txt'  # naming files sequentially starting from 1
        with open(output_file_name, 'w', encoding='utf-8') as file:
             response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
             file.write(text)
             file.write("\n")
             sent = "Sentiment: " + str(response['Sentiment']) + "  Sentiment Score:  " + str(response['SentimentScore'])
             file.write(sent)


############# Function ends here ############

user_choice = get_user_choice()

# Create a comprehend endpoint for sentiment analysis
comprehend = boto3.client('comprehend', region_name='ap-southeast-1')


# Setting the parameters to handle Tamil posts
source_language = 'ta'
target_language = 'en'

if user_choice == 1:

	# Source Excel file
	# file_name='socMed-M23-J24.xlsx'
	file_name='sm-mj.xlsx'
	
	# for pandas version >= 0.21.0
	sheet_to_df_map = pd.read_excel(file_name, sheet_name=None)
	
	# this will read the first sheet into df
	# df = pd.read_excel(file_name)
	# print(df)
	
	xls = pd.ExcelFile(file_name)
	
	# Uncomment the following if you want to make sure all sheets are read
	# print(xls.sheet_names)
	
	sheet_to_df_map = {}
	
	sheet_name = 'Water Logging '
	#print(xls.parse('Water Logging '))
	sheet_to_df_map[sheet_name] = xls.parse(sheet_name)
	i = 0
	j = 0
	for row in sheet_to_df_map[sheet_name].itertuples(index=True, name='Pandas'):
		i = i+1
		output_file_name = f'./grievances_e/file_{i}.txt'  # naming files sequentially starting from 1
		with open(output_file_name, 'w', encoding='utf-8') as file:
			#print(str(row[7]))
			file.write(str(row[7])+'\n')
			detected_language = detect_language(str(row[8]))
			if detected_language == "ta":
				#j = j + 1
				#print(j, "=== ", str(row[8]))
				translated_text = translate_text(str(row[8]), source_language, target_language)
				response = comprehend.detect_sentiment(Text=translated_text, LanguageCode='en')
				#print(f"Translated text: {translated_text}")
				file.write(translated_text)
				file.write("\n")
				sent = "Sentiment: " + str(response['Sentiment']) + "  Sentiment Score:  " + str(response['SentimentScore'])
				file.write(sent)
			else:
				response = comprehend.detect_sentiment(Text=str(row[8]), LanguageCode='en')
				file.write(str(row[8]))
				file.write("\n")
				sent = "Sentiment: " + str(response['Sentiment']) + "  Sentiment Score:  " + str(response['SentimentScore'])
				file.write(sent)
				#print(type(row[8]), "--- ", row[8])

elif user_choice == 2:
     process_image_files("./images/")
