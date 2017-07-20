from xml.dom import minidom
from xml.etree import ElementTree
import boto3
import smtplib
from datetime import datetime


def lambda_handler(event, context):
    startTime = datetime.now()


    global f
    f = open('/tmp/log.txt', 'w')
    s3_client = boto3.client('s3')
    for record in event['Records']:
        bucket = "gen3-interns-trigger"
        key = "Battleship_02392_VZ_R_NBC.xml"
        response = s3_client.get_object(Bucket=bucket, Key=key)
        file_content = response['Body'].read().decode('utf-8')
        print(bucket, key, response)
        xml_file = minidom.parseString(file_content)
        output = (validateClass(xml_file, key))

    f.write("RUNTIME=  "+ str(datetime.now() - startTime ))
    f.close()
    s3_client.upload_file('/tmp/log.txt', 'gen3-interns', 'logs/log.txt')


def validateClass(xml_file, xml_file_name):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("testintegrate2017@gmail.com", "Terminator90!")

    msg = 'Hi, The XML you sent us is invalid for the following reason(s):\n'
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
        f.write('Valid')
        msg = 'File is valid!'
        server.sendmail("testintegrate2017@gmail.com", "traffens@gmu.edu", msg)
        server.quit()
    else:
        if r1!=1:
            data=xml_file_name+" is Missing Package\n"
            f.write(data)
            msg+=str(data)
        if r2!=1:
            data=xml_file_name+" is Missing Title\n"
            f.write(data)
            msg+=str(data)
        if r3!=1:
            data=xml_file_name+" is Missing Movie\n"
            f.write(data)
        if r4!=1:
            data=xml_file_name+" is Missing Preview\n"
            f.write(data)
        if r5!=1:
            data=xml_file_name+" is Missing Poster\n"
            f.write(data)
        if r6!=1:
            data=xml_file_name+" is Missing Box Cover\n"
            f.write(data)
        if r7!=1:
            data=xml_file_name+" is Missing Thumbnail\n"
            f.write(data)
        if r8!=1:
            data=xml_file_name+" is Missing High Res\n"
            f.write(data)
        server.sendmail("testintegrate2017@gmail.com", "traffens@gmu.edu", msg)
        server.quit()

    return "Finished\n"
