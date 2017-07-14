import boto3
import os
# Let's use Amazon S3
s3 = boto3.resource('s3')
for file in os.listdir("../media"):
    print(file)
    data = open("../media/"+file, 'rb')
    s3.Bucket('gen3-interns-trigger').put_object(Key=file, Body=data)
