import boto3
import botocore
import time
s3 = boto3.resource('s3')
client = boto3.client('s3')
def checkLog():
    try:
        s3.Object('gen3-interns', 'logs/log.txt').load()
    except botocore.exceptions.ClientError as e:
        print('404 file not found')
        if e.response['Error']['Code'] == "404":
            return False
        else:
            raise
    else:
        return True


while(True):
    time.sleep(2)
    if(checkLog()):
        print('file found')
        try:
            s3.Bucket('gen3-interns').download_file('logs/log.txt', '../logs/log.txt')
            print('file downloaded')
            client.delete_object(Bucket='gen3-interns', Key ='logs/log.txt')
            print('file deleted')
            file = open('../logs/log.txt')
            print(file.read())
            file.close()
        except botocore.exceptions.ClientError as e:
            print('404 file not found')
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise
