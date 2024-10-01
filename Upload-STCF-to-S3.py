import os
import boto3
from botocore.exceptions import NoCredentialsError

# Set up AWS credentials and S3 bucket name
bucket_name = 'gcc-x-stc'  # Replace with your S3 bucket name

# Initialize a session using Amazon S3
s3 = boto3.client('s3')

def upload_folder_to_s3(folder_path, bucket_name):
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            # Construct the full local path
            local_path = os.path.join(root, filename)
            
            # Construct the S3 object key (removing the base folder path)
            relative_path = os.path.relpath(local_path, folder_path)
            s3_path = relative_path.replace("\\", "/")  # Replace backslashes with forward slashes for S3

            try:
                # Upload file to S3
                s3.upload_file(local_path, bucket_name, s3_path)
                print(f"Uploaded {local_path} to s3://{bucket_name}/{s3_path}")
            except FileNotFoundError:
                print(f"File not found: {local_path}")
            except NoCredentialsError:
                print("Credentials not available")
            except Exception as e:
                print(f"Error uploading {filename}: {str(e)}")

# Example usage
folder_path = './tweets'  # Replace with your folder path
upload_folder_to_s3(folder_path, bucket_name)

