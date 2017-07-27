#######################################################################################################
# End to end local script for internship project 2017                                                 #
# Programmed by: Michael Vanderlyn, Tyler Raffensperger                                               #
# Purpose:                                                                                            #
#     Gatekeeper code for gen3 intake of content provider packages. Takes in xml files, sends them to #
# a lambda function where they are validated and then either the content providers are alerted upon   #
# a malformed XML, or the XML is properly validated and sent back to the local script which moves the #
# content provider's package on to the normal gen3 intake process and the file is properly ingested   #
# into the VDMS system.                                                                               #
##################################################<IMPORTS>############################################
import boto3
import os, time
import botocore
import shutil
import sys
from datetime import tzinfo, timedelta, datetime
from dateutil import parser
from xml.dom import minidom
from xml.etree import ElementTree
from shutil import copyfile
s3 = boto3.resource('s3')
client = boto3.client('s3')
path_to_watch = "../../xmls_in/"
before = dict ([(f, None) for f in os.listdir (path_to_watch)])
###############################################<FUNCTIONS>############################################

######################################################################################################
def main(input_file = None):
# Main function runs all sub functions to watch a directory, send files up to lambda and listen
# until lambda sends back validation info
    #print(input_file)
    print("Searching for new files...")
    while 1:
        start_time = datetime.now()
        watch_info = watch_dir(input_file)
        if(watch_info):
            file_content_successes = False
            file_content_failures = False
            print("Processing...")
            wait_time = 0
            while(not (file_content_successes or file_content_failures)):
                wait_time +=1
                if(wait_time < 100):
                    file_content_successes = pull_from_s3_success(watch_info[0],watch_info[1])
                    file_content_failures = pull_from_s3_failures(watch_info[0],watch_info[1], watch_info[2])
                    continue
                else:
                    print("Error: No response from lambda, request timed out")
                    print("Searching for new files...")
                    break

            if(file_content_successes):
                end_time = datetime.now()
                headers = file_content_successes[0].split(",")
                headers.append("run_time")
                info = file_content_successes[1].split(",")
                lambda_start_time = parser.parse(info[len(info)-1])
                run_time = end_time - start_time
                info.append(str(run_time)+" seconds")
                print_info(headers,info)
                print("Searching for new files...")
            if(file_content_failures):
                end_time = datetime.now()
                headers = file_content_failures[0].split(",")
                headers.append("run_time")
                info = file_content_failures[1].split(",")
                lambda_start_time = parser.parse(info[len(info)-1])
                run_time = end_time - start_time
                info.append(str(run_time)+" seconds")
                print_info(headers,info)
                print("Searching for new files...")
        time.sleep(1)
def watch_dir(input_file = ""):
# listens to the xmls_in folder for new files, or removed files. If a new file is found
# it will check the content provider and then move the package to a different folder
# while it waits to be validated
### Either returns nothing because no new activity was found, or returns the content provider and package name in an array
    if(not input_file):
        global path_to_watch
        global before
        after = dict ([(f, None) for f in os.listdir (path_to_watch)])
        added = [f for f in after if not f in before]
        removed = [f for f in before if not f in after]
        file = None
    else:
        added = True
    if added:
        for filename in os.listdir("../../xmls_in/"):
            if filename.endswith(".xml"):
                if(not input_file):
                    file = ", ".join(added)
                else:
                    file = input_file
            else:
                continue



        #if(not input_file):
    #        file = ", ".join(added)
    #    else:
    #        file = input_file


        print("Upload started: "+file)
        data = open("../../xmls_in/"+file, 'rb')
        s3.Bucket('gen3-interns-trigger').put_object(Key=file, Body=data)
        print("Upload Complete")
        before = dict ([(f, None) for f in os.listdir (path_to_watch)])
        xml_file = minidom.parse("../../xmls_in/"+file)
        itemlist = xml_file.getElementsByTagName('App_Data')
        if(itemlist):
            s =itemlist[0]
            content_provider=(s.attributes['Value'].value)
        else:
            content_provider = ''
        if not(content_provider == 'nbcuniversal'):
            content_provider = "viacom"
        else:
            content_provider = "nbcuniversal"
        package_name = file.replace(".xml","")
        #Make a folder with package name
        if not os.path.exists('../../xmls_out/'+content_provider+'/'+package_name):
            os.makedirs('../../xmls_in/'+package_name)
            copyfile("../../xmls_in/" + file, "../../xmls_in/" + package_name +"/" + file) #move file into folder
            for filename in os.listdir("../../xmls_in/"):
                #if filename.contains(package_name):
                if os.path.isdir("../../xmls_in/"+filename):
                    continue
                if package_name not in filename:
                    continue
                else:
                    copyfile("../../xmls_in/" + filename, "../../xmls_in/" + package_name +"/" + filename) #move file into folder
                    os.remove("../../xmls_in/" + filename)

            ###copyfile("../../xmls_in/" + file,)

            os.makedirs('../../xmls_out/'+content_provider+'/'+package_name)
            os.rename("../../xmls_in/"+package_name,'../../xmls_out/'+content_provider+'/'+package_name)

        else:
            print("Error: "+package_name+" already in xml_out, removing and trying again")
            shutil.rmtree('../../xmls_out/'+content_provider+'/'+package_name)
            main(package_name)
        obj = s3.Object(bucket_name='gen3-interns-trigger', key=file)
        return [content_provider,package_name,obj.last_modified]
    #if removed:
        #print "Removed: ", ", ".join (removed)
    before = after





def pull_from_s3_success(content_provider,package_name):
# Checks the s3 bucket where successfully validated xmls are for new information
# if a file is here that means it was validated, and the package is good to go on to
# the rest of the gen3 ingest process.
### Returns either an array with the file headers and the file content found in the field, or false
    if(checkLog('gen3-interns-'+content_provider+'total',''+package_name+'_logs.txt')):
        print('New validation info found for a valid XML')
        try:
            s3.Bucket('gen3-interns-'+content_provider+'total').download_file(''+package_name+'_logs.txt', '../../xmls_out/'+content_provider+'/'+package_name+'/'+package_name+'_logs.txt') #add LOG to the end
            if(os.path.exists('../../xmls_out/'+content_provider+'/invalid/'+package_name)):
                shutil.rmtree('../../xmls_out/'+content_provider+'/invalid/'+package_name)
                #maybe make this so it moves the package, then writes over the xml
            try:
                os.rename('../../xmls_out/'+content_provider+'/'+package_name , '../../xmls_out/'+content_provider+'/valid/'+package_name) #moves package folder into success or failure
            except:
                shutil.rmtree('../../xmls_out/'+content_provider+'/valid/'+package_name)
                os.rename('../../xmls_out/'+content_provider+'/'+package_name , '../../xmls_out/'+content_provider+'/valid/'+package_name) #moves package folder into success or failure
            #os.rename('../../xmls_out/'+content_provider+'/'+package_name , '../../xmls_out/'+content_provider+'/valid/'+package_name) #moves package folder into success or failure
            print('Validation info retrieved from s3, shows a validation success')
            client.delete_object(Bucket='gen3-interns-'+content_provider+'total', Key =''+package_name+'_logs.txt')
            print('Old validation info deleted from s3')
            file = open('../../xmls_out/'+content_provider+'/valid/'+package_name+'/'+package_name+'_logs.txt') #add LOG to the end
            file_headers = file.readline()
            file_content =  file.readline()
            file.close()
            os.remove('../../xmls_in/'+package_name+'.xml')
            return [file_headers,file_content]
        except botocore.exceptions.ClientError as e:
            print('No new validation info')
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
                return False
            else:
                #raise
                print("Error Occured in downloading file, please try again")
                raise
def pull_from_s3_failures(content_provider,package_name, start_time):
# Checks the s3 bucket for failed xml files. If any packages xml is here that means
# that the xml didn't pass validation and that the content provider and our team must be alerted
# this function also moves the package to a seperate location while it waits for our team to deal with it
### Returns either an array with the file headers and the file content found in the field, or false
    if(checkLog('gen3-interns-'+content_provider+'failures',''+package_name+'_logs.txt')):
        obj = s3.Object(bucket_name='gen3-interns-'+content_provider+'failures', key=''+package_name+'_logs.txt')
        last_mod = obj.last_modified
        if(last_mod < start_time):
            s3.meta.client.delete_object(Bucket='gen3-interns-'+content_provider+'failures', Key=''+package_name+'_logs.txt')
            print("deleted old validation info")
        else:
            print('New validation info found for an invalid XML')
            try:
                if(os.path.exists('../../xmls_out/'+content_provider+'/'+package_name+'/')):
                    s3.Bucket('gen3-interns-'+content_provider+'failures').download_file(''+package_name+'_logs.txt', '../../xmls_out/'+content_provider+'/'+package_name+'/'+package_name+'_logs.txt') #add LOG to the end
                    print("file downloaded")
                else:
                    print("Error missing folder: "+'../../xmls_out/'+content_provider+'/'+package_name+'/')
                    print("Trying again")
                    main(package_name)
                if(os.path.exists('../../xmls_out/'+content_provider+'/valid/'+package_name)):
                    shutil.rmtree('../../xmls_out/'+content_provider+'/valid/'+package_name)
                try:
                    os.renames('../../xmls_out/'+content_provider+'/'+package_name , '../../xmls_out/'+content_provider+'/invalid/'+package_name) #moves package folder into success or failure
                except:
                    shutil.rmtree('../../xmls_out/'+content_provider+'/invalid/'+package_name)
                    os.renames('../../xmls_out/'+content_provider+'/'+package_name , '../../xmls_out/'+content_provider+'/invalid/'+package_name) #moves package folder into success or failure
                    print('Validation info retrieved from s3, shows a validation failure')
                    file = open('../../xmls_out/'+content_provider+'/invalid/'+package_name+'/'+package_name+'_logs.txt') #add LOG to the end
                    file_headers = file.readline()
                    file_content =  file.readline()
                    file.close()
                    #########################os.remove('../../xmls_in/'+package_name+'.xml')
                    return [file_headers,file_content]
            except botocore.exceptions.ClientError as e:
                print('No new validation info')
                if e.response['Error']['Code'] == "404":
                    print("The object does not exist.")
                    return False
                else:
                    raise
def checkLog(bucket,key):
# Helper function to check a bucket for the specific filename (key) to see if the valication
# process is done yet. returns a boolean that is True if the key was found in the bucket
    try:
        s3.Object(bucket, key).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            return False
        else:
            raise
    else:
        return True
def print_info(headers, vals):
# Helper function to print out information for console. Makes data visualization easier
    print("#################<FILE INFO>######################")
    for i in range(len(headers)):
        line =headers[i]+": "+vals[i]
        line = line.replace("\n","")
        print(line)
    print("###################################################")
#########################################<END OF FUNCTIONS>################################################
## Runs main function
main()
