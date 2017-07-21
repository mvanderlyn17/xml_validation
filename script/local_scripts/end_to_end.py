#######################################################################################################
# End to end local script for internship project 2017                                                 #
# Programmed by: Michael Vanderlyn                                                                    #
#                 so sexy                                                                             #
##################################################<IMPORTS>############################################
import boto3
import os, time
import botocore
from datetime import datetime
from dateutil import parser

s3 = boto3.resource('s3')
client = boto3.client('s3')
path_to_watch = "../../xmls/"
before = dict ([(f, None) for f in os.listdir (path_to_watch)])

###############################################<FUNCTIONS>############################################
def main():
    #need to record information per partner in a local text file
    print("Searching for new files...")
    while 1:
        # I DON'T THINK THIS IS THE RIGHT WAY TO DO THIS, WHAT IF WE GO THROUGH ANOTHER LOOP BEFORE SEEING THE VALIDATION
        start_time = datetime.now()                            # NEED TO GET START TIME FROM FILE, END TIME IS FROM WHEN WE FINISH PROCESSING IT
        file_found = watch_dir()
        #file_content = pull_from_s3()
        if(file_found):
            file_content = False
            print("Processing...")
            while(not file_content):
                file_content = pull_from_s3()
                continue
            end_time = datetime.now()
            headers = file_content[0].split(",")
            headers.append("run_time")
            info = file_content[1].split(",")
            lambda_start_time = parser.parse(info[len(info)-1])
            run_time = end_time - start_time
            info.append(str(run_time)+" seconds")
            print_info(headers,info)
            #read file to fill variables
            #print out content provider
            #print out filename
            #print out valid/invalid
            #print out what was wrong
            #print out running partners accuracy, score
            #print run time
            print("Searching for new files...")
        time.sleep(.5)
def watch_dir():
    global path_to_watch
    global before
    global start_time
    after = dict ([(f, None) for f in os.listdir (path_to_watch)])
    added = [f for f in after if not f in before]
    removed = [f for f in before if not f in after]
    if added:
        file = ", ".join(added)
        print("Upload started: "+file)
        data = open("../../xmls/"+file, 'rb')
        s3.Bucket('gen3-interns-trigger').put_object(Key=file, Body=data)
        print "Upload Complete"
        before = dict ([(f, None) for f in os.listdir (path_to_watch)])
        return True

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
            return [file_headers,file_content]

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

def print_info(headers, vals):
    print("#################<FILE INFO>######################")
    for i in range(len(headers)):
        line =headers[i]+": "+vals[i]
        line = line.replace("\n","")
        print(line)
    print("###################################################")

#########################################<END OF FUNCTIONS>################################################
## - run main function
main()
