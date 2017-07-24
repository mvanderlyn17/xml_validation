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
            file_content_successes = False
            file_content_failures = False
            print("Processing...")
            while(not (file_content_successes or file_content_failures)):
                file_content_successes = pull_from_s3_success(watch_info[0],watch_info[1])
                file_content_failures = pull_from_s3_failures(watch_info[0],watch_info[1])
                print("successes: "+str(file_content_successes))
                print("fialures: "+str(file_content_failures))
                continue
            if(file_content_successes):
                end_time = datetime.now()
                headers = file_content_successes[0].split(",")
                headers.append("run_time")
                info = file_content_successes[1].split(",")
                lambda_start_time = parser.parse(info[len(info)-1]) #issue here
                run_time = end_time - start_time
                info.append(str(run_time)+" seconds")
                print_info(headers,info)
                print("Searching for new files...")
            if(file_content_failures):
                end_time = datetime.now()
                headers = file_content_failures[0].split(",")
                headers.append("run_time")
                info = file_content_failures[1].split(",")
                lambda_start_time = parser.parse(info[len(info)-1]) #issue here
                run_time = end_time - start_time
                info.append(str(run_time)+" seconds")
                print_info(headers,info)
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
            content_provider = "viacom"
        else:
            content_provider = "nbc"
        package_name = file.replace(".xml","")


        print(content_provider)
        os.rename("../../xmls_in/" + file, "../../xmls_out/" + content_provider +"/" + file)

        return [content_provider,package_name]

    if removed:
        print "Removed: ", ", ".join (removed)
    before = after



def pull_from_s3_success(content_provider,package_name):
    if(checkLog('gen3-interns-'+content_provider+'total',''+package_name+'.txt')):
        print('New validation info found')
        try:
            s3.Bucket('gen3-interns-'+content_provider+'total').download_file(''+package_name+'.txt', '../../xmls_out/'+content_provider+'/'+package_name+'.txt') #add LOG to the end
            print('Validation info retrieved from s3')
            print('Validation info retrieved from s3, shows a validation success')
            client.delete_object(Bucket='gen3-interns-'+content_provider+'total', Key ='logs/'+package_name+'.txt')
            print('Old validation info deleted from s3')
            file = open('../../xmls_out/'+content_provider+'/'+package_name+'.txt') #add LOG to the end
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

def pull_from_s3_failures(content_provider,package_name):
    if(checkLog('gen3-interns-'+content_provider+'failures',''+package_name+'.txt')):
        print('New validation info found')
        try:
            s3.Bucket('gen3-interns-'+content_provider+'failures').download_file(''+package_name+'.txt', '../../xmls_out/'+content_provider+'/'+package_name+'.txt') #New folder for failed xml packages
            print('Validation info retrieved from s3, shows a validation failure')
            print('Validation failed info stored in s3')
            file = open('../../xmls_out/'+content_provider+'/'+package_name+'.txt') #add LOG to the end
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

def checkLog(bucket,key):
    try:
        s3.Object(bucket, key).load()
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
