import boto3
import time
from botocore.exceptions import NoCredentialsError

# Initialize a session using Spaces
session = boto3.session.Session()

cloudwatch = boto3.client('cloudwatch')
s3 = session.client('s3',
                    region_name='region_name',
                    endpoint_url='endpoint_url',
                    aws_access_key_id='access_key',
                    aws_secret_access_key='secret_key')


def upload_to_aws(local_file, bucket, s3_file):
    try:
        start = time.time()
        s3.upload_file(local_file, bucket, s3_file)
        end = time.time()
        duration = end - start
        print("Upload Successful")

        # Send custom metrics to CloudWatch
        cloudwatch.put_metric_data(
            Namespace='S3Uploader',
            MetricData=[
                {
                    'MetricName': 'UploadTime',
                    'Dimensions': [
                        {
                            'Name': 'FileName',
                            'Value': s3_file
                        },
                    ],
                    'Unit': 'Seconds',
                    'Value': duration
                },
            ]
        )

        return duration
    except FileNotFoundError:
        print("The file was not found")
        return None
    except NoCredentialsError:
        print("Credentials not available")
        return None


def download_from_aws(bucket, s3_file, local_file):
    try:
        s3.download_file(bucket, s3_file, local_file)
        print("Download Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


def delete_from_aws(bucket, s3_file):
    try:
        s3.delete_object(Bucket=bucket, Key=s3_file)
        print("Delete Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


# Create a s3 bucket
s3.create_bucket(Bucket='mega_bucket')

# Upload a text file
upload_time = upload_to_aws('mega_file', 'mega_bucket', 'mega_file.txt')

# Download the same text file
download_from_aws('mega_bucket', 'mega_file.txt', 'mega_file')

# Delete the text file
delete_from_aws('mega_bucket', 'mega_file.txt')

# Print the time taken to upload the file
print(f"Time taken to upload file: {upload_time} seconds")
