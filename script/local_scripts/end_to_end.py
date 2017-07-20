#######################################################################################################
# End to end local script for internship project 2017                                                 #
# Programmed by: Michael Vanderlyn                                                                    #
#                                                                                                     #
##################################################<IMPORTS>############################################
import boto3
import os, time
import botocore
s3 = boto3.resource('s3')
client = boto3.client('s3')
path_to_watch = "../../xmls/"
before = dict ([(f, None) for f in os.listdir (path_to_watch)])
###############################################<FUNCTIONS>############################################
def main():

    while 1:
        watch_dir()
        pull_from_s3()
        time.sleep(2)
def watch_dir():
    global path_to_watch
    global before
    after = dict ([(f, None) for f in os.listdir (path_to_watch)])
    added = [f for f in after if not f in before]
    removed = [f for f in before if not f in after]
    if added:
        file = ", ".join(added)
        print("Upload started: "+file)
        data = open("../../xmls/"+file, 'rb')
        s3.Bucket('gen3-interns-trigger').put_object(Key=file, Body=data)
        print "Uploaded Complete"
    if removed:
        print "Removed: ", ", ".join (removed)
    before = after
def pull_from_s3():
    time.sleep(2)
    if(checkLog()):
        print('file found')
        try:
            s3.Bucket('gen3-interns').download_file('logs/log.txt', '../../logs/log.txt')
            print('file downloaded')
            client.delete_object(Bucket='gen3-interns', Key ='logs/log.txt')
            print('file deleted')
            file = open('../../logs/log.txt')
            print(file.read())
            file.close()
        except botocore.exceptions.ClientError as e:
            print('404 file not found')
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise
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
#########################################<END OF FUNCTIONS>################################################
## - run main function
main()
