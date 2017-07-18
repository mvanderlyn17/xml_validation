from xml.dom import minidom
from xml.etree import ElementTree
import boto3
def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    for record in event['Records']:
        #bucket = record['s3']['bucket']['name']
        bucket = "gen3-interns-trigger" #TEST LINE SHOULD BE TAKEN FROM EVEN TRIGGER
        #key = record['s3']['object']['key']
        key = "Battleship_02392_VZ_R_NBC.xml" # TEST LINE SHOULD BE TAKEN FROM EVENT TRIGGER IN THE END
        response = s3_client.get_object(Bucket=bucket, Key=key) # NEED TO FIGURE OUT WHAT TO DO WHEN OBJECT ISN'T public, maybe should look at the IAM roles
        file_content = response['Body'].read().decode('utf-8')
        print(bucket, key, response)
        xml_file = minidom.parse(file_content)
        validateClass(xml_file)

def validateClass(xml):

    #wfile=open("Demo.txt","a+")
    data=" "
    r=0
    r1=0
    r2=0
    r3=0
    r4=0
    r5=0
    r6=0
    r7=0
    r8=0
    xmldoc = minidom.parse(xml)
    itemlist = xmldoc.getElementsByTagName('AMS')
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
        return "Valid"
    else:
        if r1!=1:
            data=xmlfilename+" is Missing Package\n\n"
           # wfile.write(data)
            return "Invalid"
        if r2!=1:
            data=xmlfilename+" is Missing Title\n\n"
          #  wfile.write(data)
            return "Invalid"
        if r3!=1:
            data=xmlfilename+" is Missing Movie\n\n"
           # wfile.write(data)
            return "Invalid"
        if r4!=1:
            data=xmlfilename+" is Missing Preview\n\n"
           # wfile.write(data)
            return "Invalid"
        if r5!=1:
            data=xmlfilename+" is Missing Poster\n\n"
            #wfile.write(data)
            return "Invalid"
        if r6!=1:
            data=xmlfilename+" is Missing Box Cover\n\n"
           # wfile.write(data)
            return "Invalid"
        if r7!=1:
            data=xmlfilename+" is Missing Thumbnail\n\n"
           # wfile.write(data)
            return "Invalid"
        if r8!=1:
            data=xmlfilename+" is Missing High Res\n\n"
           # wfile.write(data)
            return "Invalid"


