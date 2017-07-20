import boto3
import os
############################<TEST FUNCTION TO UPLOAD ALL XMLS TO S3>############################
################################################################################################
################################################################################################

s3 = boto3.resource('s3')
for file in os.listdir("../xmls"):
    print(file)
    data = open("../xmls/"+file, 'rb')
    s3.Bucket('gen3-interns-trigger').put_object(Key=file, Body=data)
