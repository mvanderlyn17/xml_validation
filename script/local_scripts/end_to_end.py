#######################################################################################################
# End to end local script for internship project 2017                                                 #
# Programmed by: Michael Vanderlyn                                                                    #
#                 so sexy                                                                             #
##################################################<IMPORTS>############################################
import boto3
import os, time
import botocore
from datetime import datetime


s3 = boto3.resource('s3')
client = boto3.client('s3')
path_to_watch = "../../xmls/trigger/"
before = dict ([(f, None) for f in os.listdir (path_to_watch)])
###############################################<FUNCTIONS>############################################
def main():
    #need to record information per partner in a local text file
    while 1:
        startTime = datetime.now()
        watch_dir()
<<<<<<< HEAD
        file_content = pull_from_s3()
        if(file_content):
            headers = file_content[0].split(",")
            info = file_content[1].split(",")
            print(''.join(headers))
            print(info)
            #read file to fill variables
            #print out content provider
            #print out filename
            #print out valid/invalid
            #print out what was wrong
            #print out running partners accuracy, score
            #print run time
=======
        x = pull_from_s3()
        if(x):
            file = open('../../logs/log.txt', 'a')
            endTime = datetime.now()
            runTime = endTime - startTime
            file.write('\n\nTOTAL RUNTIME: '+ str(runTime) + '\n\n')
            file.close()
>>>>>>> ac759c4872b6c7787399945b0339542be3b87fa9
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
        print "Upload Complete"

    if removed:
        print "Removed: ", ", ".join (removed)
    before = after



def pull_from_s3():
    if(checkLog()):
        print('New validation info found')
        try:
            s3.Bucket('gen3-interns').download_file('logs/log.txt', '../../logs/log.txt')
            print('Validation info retrieved from s3')
            client.delete_object(Bucket='gen3-interns', Key ='logs/log.txt')
            print('Old validation info deleted from s3')
            file = open('../../logs/log.txt')
            #print(file.read())
            file_headers = file.readline()
            file_content =  file.readline()
            file.close()
<<<<<<< HEAD
            return [file_headers,file_content]
=======
            return True
>>>>>>> ac759c4872b6c7787399945b0339542be3b87fa9
        except botocore.exceptions.ClientError as e:
            print('No new validation info')
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
                return False
            else:
                raise



def checkLog():
    try:
        s3.Object('gen3-interns', 'logs/log.txt').load()
    except botocore.exceptions.ClientError as e:
        #print('404 file not found')
        if e.response['Error']['Code'] == "404":
            return False
        else:
            raise
    else:
        return True
#########################################<END OF FUNCTIONS>################################################
## - run main function
main()
