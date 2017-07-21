#######################################################################################################
# End to end local script for internship project 2017                                                 #
# Programmed by: nylrednaV leahciM                                                                    #
#                 so sexy                                                                             #
##################################################<IMPORTS>############################################
import boto3
import os, time
import botocore
from datetime import datetime
from dateutil import parser
from xml.dom import minidom
from xml.etree import ElementTree
s3 = boto3.resource('s3')
client = boto3.client('s3')
path_to_watch = "../../xmls_in/"
before = dict ([(f, None) for f in os.listdir (path_to_watch)])

###############################################<FUNCTIONS>############################################
def main():
    #need to record information per partner in a local text file
    print("Searching for new files...")
    while 1:
        start_time = datetime.now()
        watch_info = watch_dir()
        if(watch_info):
            file_content = False
            print("Processing...")
            while(not file_content):
                file_content = pull_from_s3(watch_info[0],watch_info[1])
                #print('oh dear')
                continue
            end_time = datetime.now()
            headers = file_content[0].split(",")
            headers.append("run_time")
            info = file_content[1].split(",")
            lambda_start_time = parser.parse(info[len(info)-1])  #ERROR HERE WHEN INVALID
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
        data = open("../../xmls_in/"+file, 'rb')
        s3.Bucket('gen3-interns-trigger').put_object(Key=file, Body=data)
        print "Upload Complete"
        before = dict ([(f, None) for f in os.listdir (path_to_watch)])
        #print(data)
        #print(info)
        #print(file.read().decode('utf-8'))

        xml_file = minidom.parse("../../xmls_in/"+file)
        itemlist = xml_file.getElementsByTagName('App_Data')
        s =itemlist[0]
        content_provider=(s.attributes['Value'].value)
        if not(content_provider == 'nbcuniversal'):
            content_provider = "other"
        package_name = file.replace(".xml","")



        os.rename("../../xmls_in/" + file, "../../xmls_out/" + content_provider +"/" + file)

        return [content_provider,package_name]

    if removed:
        j=2
        #print "Removed: ", ", ".join (removed)
    before = after



def pull_from_s3(content_provider,package_name):
    if(checkLog(package_name)):
        print('New validation info found')
        try:
            s3.Bucket('gen3-interns').download_file('logs/'+package_name+'.txt', '../../xmls_out/'+content_provider+'/'+package_name+'.txt') #add LOG to the end
            #print('Validation info retrieved from s3')
            client.delete_object(Bucket='gen3-interns', Key ='logs/'+package_name+'.txt')
            #print('Old validation info deleted from s3')
            file = open('../../xmls_out/'+content_provider+'/'+package_name+'.txt') #add LOG to the end
            file_headers = file.readline()
            file_content =  file.readline()
            file.close()
            return [file_headers, file_content]


        except botocore.exceptions.ClientError as e:
            print('No new validation info')
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
                return False
            else:
                raise


def checkLog(package_name):
    try:
        s3.Object('gen3-interns', 'logs/'+package_name+'.txt').load()
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
