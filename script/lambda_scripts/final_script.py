#######################################################################################################
# Lambda script for internship project 2017                                                           #
# Programmed by: Michael Vanderlyn, Tyler Raffesnperger, Saumya Shukla, Sairaj Alve                   #
# Purpose:                                                                                            #
#     Gatekeeper code for gen3 intake of content provider packages. Takes in xml files, validates     #
# then sends back validation info to local script. Also alerts content providers and team members     #
# and generates reports based on the information.                                                     #
##################################################<IMPORTS>############################################
from xml.dom import minidom
from xml.etree import ElementTree
import boto3
import smtplib
from datetime import datetime
from random import randint
###############################################<FUNCTIONS>############################################
def lambda_handler(event, context):
# Main function, called when a new xml is sent to the gen3-trigger bucket. When triggered information on
# the xml is sent to the function via a json being passed to the event parameter, and the filename and bucket
# are extracted from the event json. Then the xml is either validated with viacom or nbc validation scripts
# after this if its validated its moved to the validated bucket for its content provider, otherwise its
# moved to a seperate bucket for failed xmls for that content provider, and emails are sent out to notify
# our team and the content provider
    start_time = datetime.now()
    global f
    s3_client = boto3.client('s3')
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        print("key: "+key)
        response = s3_client.get_object(Bucket=bucket, Key=key)
        print("got: "+key)
        s3_client.delete_object(Bucket=bucket, Key=key)
        file_content = response['Body'].read().decode('utf-8')
        xml_file = minidom.parseString(file_content)
        itemlist = xml_file.getElementsByTagName('App_Data')
        s =itemlist[0]
        content_provider=(s.attributes['Value'].value)
        output = (validateClass(xml_file, key))
        package_name = key.replace(".xml","")
        validity_status = output[0]
        invalid_fields = output[1]
        if(len(invalid_fields)<=0):
            invalid_fields = "[]"
        else:
            invalid_fields = "".join(invalid_fields)
        f = open('/tmp/'+package_name+'.txt', 'w')
        f.write('content_provider,package_name,validity_status,invalid_fields,lambda_start_time\n'+content_provider+","+package_name+","+validity_status+","+invalid_fields+","+str(start_time))
        f.close()
       if(content_provider =="nbcuniversal"):
            if(validity_status =="Valid"):
                s3_client.upload_file('/tmp/'+package_name+'.txt', 'gen3-interns-nbctotal', ''+package_name+'.txt')
            else:
                s3_client.upload_file('/tmp/'+package_name+'.txt', 'gen3-interns-nbcfailures', ''+package_name+'.txt')
        else:
            if(validity_status =="Valid"):
                s3_client.upload_file('/tmp/'+package_name+'.txt', 'gen3-interns-viacomtotal', ''+package_name+'.txt')
            else:
                s3_client.upload_file('/tmp/'+package_name+'.txt', 'gen3-interns-viacomfailures', ''+package_name+'.txt')
def validateClass(xml_file, xml_file_name):
# Validates an xml will be split up into 2 functions one for each content provider
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("testintegrate2017@gmail.com", "Terminator90!")
    s3_client = boto3.client('s3')
    r1,r2,r3,r4,r5,r6,r7,r8=0,0,0,0,0,0,0,0
    itemlist = xml_file.getElementsByTagName('AMS')
    for s in itemlist:
        values=(s.attributes['Asset_Class'].value)
        if values=="package":
            r1=1
        elif values=="title":
            r2=1
        elif values=="movie":
            r3=1
        elif values=="preview":
            r4=1
        elif values=="poster":
            r5=1
        elif values=="box cover":
            r6=1
        elif values=="thumb nail":
            r7=1
        elif values=="high res":
            r8=1
        else:
            continue
    if r1==1 and r2==1 and r3==1 and r4==1 and r5==1 and r6==1 and r7==1 and r8==1:
        msg = 'File is valid!'
        server.sendmail("testintegrate2017@gmail.com", "michael.vanderlyn@verizondigitalmedia.com", msg)
        server.quit()
        return ["Valid",[]]
    else:
        missing_fields = []
        missing_fields.append('The XML you sent us is invalid for the following reason(s)..  \n\n ')
        if r1!=1:
            data=xml_file_name+" is Missing Asset Class" #asset class missing
            missing_fields.append(data)
        if r2!=1:
            data=xml_file_name+" is Missing Title"
            missing_fields.append(data)
        if r3!=1:
            data=xml_file_name+" is Missing Movie"
            missing_fields.append(data)
        if r4!=1:
            data=xml_file_name+" is Missing Preview"
            missing_fields.append(data)
        if r5!=1:
            data=xml_file_name+" is Missing Poster"
            missing_fields.append(data)
        if r6!=1:
            data=xml_file_name+" is Missing Box Cover"
            missing_fields.append(data)
        if r7!=1:
            data=xml_file_name+" is Missing Thumbnail"
            missing_fields.append(data)
        if r8!=1:
            data=xml_file_name+" is Missing High Res"
            missing_fields.append(data)
        email =  str('\n'.join([str(x) for x in missing_fields]))
        server.sendmail("testintegrate2017@gmail.com", "michael.vanderlyn@verizondigitalmedia.com", email)
        server.quit()
        del missing_fields[0]
        return ['Invalid',missing_fields]




#from xml.dom import minidom
#from xml.etree import ElementTree
#import boto3
#import smtplib
#from datetime import datetime


#def lambda_handler(event, context):
#    startTime = datetime.now()


#    global f
#    f = open('/tmp/log.txt', 'w')
#    s3_client = boto3.client('s3')
#    for record in event['Records']:
        #bucket = record['s3']['bucket']['name']
#        bucket = "gen3-interns-trigger" #TEST LINE INFO SHOULD BE TAKEN FROM EVEN TRIGGER
#        #key = record['s3']['object']['key']
#        key = "Battleship_02392_VZ_R_NBC.xml" # TEST LINE INFO SHOULD BE TAKEN FROM EVENT TRIGGER
#        response = s3_client.get_object(Bucket=bucket, Key=key)
#        file_content = response['Body'].read().decode('utf-8')
#        print(bucket, key, response)
#        xml_file = minidom.parseString(file_content)
#        output = (validateClass(xml_file, key))

#    f.write("RUNTIME=  "+ str(datetime.now() - startTime ))
#    f.close()
#    s3_client.upload_file('/tmp/log.txt', 'gen3-interns', 'logs/log.txt')


#def validateClass(xml_file, xml_file_name):
#    server = smtplib.SMTP('smtp.gmail.com', 587)
#   server.starttls()
#    server.login("testintegrate2017@gmail.com", "Terminator90!")

#    msg = 'Hi, The XML you sent us is invalid for the following reason(s):\n'
#    s3_client = boto3.client('s3')
#    r1,r2,r3,r4,r5,r6,r7,r8=0,0,0,0,0,0,0,0
#    itemlist = xml_file.getElementsByTagName('AMS')


#    for s in itemlist:

#        values=(s.attributes['Asset_Class'].value)
#        if values=="package":
#            r1=1
#        elif values=="title":
#             r2=1
#        elif values=="movie":
#            r3=1
#        elif values=="preview":
#            r4=1
#        elif values=="poster":
#            r5=1
#        elif values=="box cover":
#            r6=1
#        elif values=="thumb nail":
#            r7=1
#        elif values=="high res":
#            r8=1
#        else:
#            continue


#    if r1==1 and r2==1 and r3==1 and r4==1 and r5==1 and r6==1 and r7==1 and r8==1:
#        f.write('Valid')
#        msg = 'File is valid!'
#        server.sendmail("testintegrate2017@gmail.com", "traffens@gmu.edu", msg)
#        server.quit()
#    else:
#        if r1!=1:
#            data=xml_file_name+" is Missing Package\n"
#            f.write(data)
#            msg+=str(data)
#        if r2!=1:
#            data=xml_file_name+" is Missing Title\n"
#            f.write(data)
#            msg+=str(data)
#        if r3!=1:
#            data=xml_file_name+" is Missing Movie\n"
#            f.write(data)
#        if r4!=1:
#            data=xml_file_name+" is Missing Preview\n"
#            f.write(data)
#        if r5!=1:
#            data=xml_file_name+" is Missing Poster\n"
#            f.write(data)
#        if r6!=1:
#            data=xml_file_name+" is Missing Box Cover\n"
#            f.write(data)
#        if r7!=1:
#            data=xml_file_name+" is Missing Thumbnail\n"
#            f.write(data)
#        if r8!=1:
#            data=xml_file_name+" is Missing High Res\n"
#            f.write(data)
#        server.sendmail("testintegrate2017@gmail.com", "traffens@gmu.edu", msg)
#        server.quit()

#    return "Finished\n"


# from xml.dom import minidom
# from xml.etree import ElementTree
# import boto3
# import smtplib
# from datetime import datetime
# from random import randint
#
#
# def lambda_handler(event, context):
#     start_time = datetime.now()
#
#
#     global f
#     s3_client = boto3.client('s3')
#     for record in event['Records']:
#         bucket = record['s3']['bucket']['name']
#         #bucket = "gen3-interns-trigger" #TEST LINE SHOULD BE TAKEN FROM EVEN TRIGGER
#         key = record['s3']['object']['key']
#         #key = "Battleship_02392_VZ_R_NBC.xml" # TEST LINE SHOULD BE TAKEN FROM EVENT TRIGGER IN THE END
#         print("key: "+key)
#         response = s3_client.get_object(Bucket=bucket, Key=key)
#         print("got: "+key)
#         s3_client.delete_object(Bucket=bucket, Key=key)
#
#         file_content = response['Body'].read().decode('utf-8')
#         #print(bucket, key, response)
#         xml_file = minidom.parseString(file_content)
#         itemlist = xml_file.getElementsByTagName('App_Data')
#         s =itemlist[0]
#         content_provider=(s.attributes['Value'].value)
#         output = (validateClass(xml_file, key))
#         #content_provider = "NBC" # Provider_Content_Tier"
#         package_name = key.replace(".xml","")
#         validity_status = output[0]
#         invalid_fields = output[1]
#         #g=False
#         if(len(invalid_fields)<=0):
#             invalid_fields = "[]"
#         else:
#             invalid_fields = "".join(invalid_fields)
#             #g=True
#         f = open('/tmp/'+package_name+'.txt', 'w')
#         f.write('content_provider,package_name,validity_status,invalid_fields,lambda_start_time\n'+content_provider+","+package_name+","+validity_status+","+invalid_fields+","+str(start_time))
#         #f.write('content_provider,package_name,validity_status,invalid_fields,lambda_start_time\n'+content_provider+","+package_name+","+validity_status+","+invalid_fields+","+"bitches")
#         #if(g):
#             #f.write(',12345'+str(start_time))
#         f.close()
#         #s3_client.upload_file('/tmp/'+package_name+'.txt', 'gen3-interns', 'logs/'+package_name+'.txt')
#         if(content_provider =="nbcuniversal"):
#             if(validity_status =="Valid"):
#                 s3_client.upload_file('/tmp/'+package_name+'.txt', 'gen3-interns-nbctotal', ''+package_name+'.txt')
#             else:
#                 s3_client.upload_file('/tmp/'+package_name+'.txt', 'gen3-interns-nbcfailures', ''+package_name+'.txt')
#         else:
#             if(validity_status =="Valid"):
#                 s3_client.upload_file('/tmp/'+package_name+'.txt', 'gen3-interns-viacomtotal', ''+package_name+'.txt')
#             else:
#                 s3_client.upload_file('/tmp/'+package_name+'.txt', 'gen3-interns-viacomfailures', ''+package_name+'.txt')
#
# def validateClass(xml_file, xml_file_name):
#     server = smtplib.SMTP('smtp.gmail.com', 587)
#     server.starttls()
#     server.login("testintegrate2017@gmail.com", "Terminator90!")
#
#     s3_client = boto3.client('s3')
#     r1,r2,r3,r4,r5,r6,r7,r8=0,0,0,0,0,0,0,0
#
#
#     itemlist = xml_file.getElementsByTagName('AMS')
#     for s in itemlist:
#
#         values=(s.attributes['Asset_Class'].value)
#         if values=="package":
#             r1=1
#         elif values=="title":
#             r2=1
#         elif values=="movie":
#             r3=1
#         elif values=="preview":
#             r4=1
#         elif values=="poster":
#             r5=1
#         elif values=="box cover":
#             r6=1
#         elif values=="thumb nail":
#             r7=1
#         elif values=="high res":
#             r8=1
#         else:
#             continue
#
#
#     if r1==1 and r2==1 and r3==1 and r4==1 and r5==1 and r6==1 and r7==1 and r8==1:
#         msg = 'File is valid!'
#         server.sendmail("testintegrate2017@gmail.com", "michael.vanderlyn@verizondigitalmedia.com", msg)
#
#
#         #d = str(randint(0, 99999))
#         #ds = open('/tmp/loggy.txt', 'w')
#         #ds.close()
#         #s3_client.upload_file('/tmp/loggy.txt', 'gen3-interns-nbctotal', 'filler'+d+'.txt')
#        # s3_client.upload_file('/tmp/loggy.txt', 'gen3-interns-viacomtotal', 'filler'+d+'.txt')
#
#         server.quit()
#         return ["Valid",[]]
#     else:
#         missing_fields = []
#         missing_fields.append('The XML you sent us is invalid for the following reason(s)..  \n\n ')
#
#         if r1!=1:
#             data=xml_file_name+" is Missing Asset Class" #asset class missing
#             #print('\n\n\n' + data)
#             missing_fields.append(data)
#             #print('\n\n\n'+str(missing_fields))
#         if r2!=1:
#             data=xml_file_name+" is Missing Title"
#             missing_fields.append(data)
#         if r3!=1:
#             data=xml_file_name+" is Missing Movie"
#             missing_fields.append(data)
#         if r4!=1:
#             data=xml_file_name+" is Missing Preview"
#             missing_fields.append(data)
#         if r5!=1:
#             data=xml_file_name+" is Missing Poster"
#             missing_fields.append(data)
#         if r6!=1:
#             data=xml_file_name+" is Missing Box Cover"
#             missing_fields.append(data)
#         if r7!=1:
#             data=xml_file_name+" is Missing Thumbnail"
#             missing_fields.append(data)
#         if r8!=1:
#             data=xml_file_name+" is Missing High Res"
#             missing_fields.append(data)
#
#         email =  str('\n'.join([str(x) for x in missing_fields]))
#
#
#         server.sendmail("testintegrate2017@gmail.com", "michael.vanderlyn@verizondigitalmedia.com", email)
#
#         #x = str(randint(0, 99999))
#         #sf = open('/tmp/loggy.txt', 'w')
#         #sf.close()
#         #s3_client.upload_file('/tmp/loggy.txt', 'gen3-interns-nbcfailures', 'filler'+x+'.txt')
#         #s3_client.upload_file('/tmp/loggy.txt', 'gen3-interns-viacomfailures', 'filler'+x+'.txt')
#         #s3_client.upload_file('/tmp/loggy.txt', 'gen3-interns-nbctotal', 'filler'+x+'.txt')
#         #s3_client.upload_file('/tmp/loggy.txt', 'gen3-interns-viacomtotal', 'filler'+x+'.txt')
#
#         server.quit()
#         del missing_fields[0]
#         return ['Invalid',missing_fields]
