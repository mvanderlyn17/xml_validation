from xml.dom import minidom
from xml.etree import ElementTree
import boto3
import smtplib
from datetime import datetime
import botocore

def lambda_handler(event, context):
    #startTime = datetime.now()



    global f
    f = open('/tmp/log.txt', 'w')
    s3_resource = boto3.resource('s3')
    s3_client = boto3.client('s3')
    for record in event['Records']:
        #bucket = record['s3']['bucket']['name']
        bucket = "gen3-interns-trigger" #TEST LINE SHOULD BE TAKEN FROM EVEN TRIGGER

        for keys in s3_client.list_objects(Bucket='gen3-interns-trigger')['Contents']:
            key = str(keys['Key'])


        #print(key)
        #key = "Battleship_02392_VZ_R_NBC.xml" # TEST LINE SHOULD BE TAKEN FROM EVENT TRIGGER IN THE END
        response = s3_client.get_object(Bucket=bucket, Key=key)
        file_content = response['Body'].read().decode('utf-8')
        print(bucket, key, response)
        xml_file = minidom.parseString(file_content)
        output = (validateClass(xml_file, key))
        #bucket.delete(key)




    content_provider = "NBC" # Provider_Content_Tier"
    package_name = "Battleship" #Battleship_Package
    validity_status = output[0]
    invalid_fields = output[1]
    if(len(invalid_fields)<=0):
        invalid_fields = "[]"
    else:
        invalid_fields = "".join(invalid_fields)
    f.write('content_provider,package_name,validity_status,invalid_fields\n'+content_provider+","+package_name+","+validity_status+","+invalid_fields)
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
        #f.write('Valid')
        msg = 'File is valid!'
        #server.sendmail("testintegrate2017@gmail.com", "michael.vandelryn@verizondigitalmedia.com", msg)
        server.quit()
        return ["Valid",[]]
    else:
        missing_fields = []
        if r1!=1:
            data=xml_file_name+" is Missing Package\n"
            #f.write(data)
            msg+=str(data)
            missing_fields.append(data)
        if r2!=1:
            data=xml_file_name+" is Missing Title\n"
            #f.write(data)
            msg+=str(data)
            missing_fields.append(data)
        if r3!=1:
            data=xml_file_name+" is Missing Movie\n"
            #f.write(data)
            missing_fields.append(data)
        if r4!=1:
            data=xml_file_name+" is Missing Preview\n"
            #f.write(data)
            missing_fields.append(data)
        if r5!=1:
            data=xml_file_name+" is Missing Poster\n"
            #f.write(data)
            missing_fields.append(data)
        if r6!=1:
            data=xml_file_name+" is Missing Box Cover\n"
            #f.write(data)
            missing_fields.append(data)
        if r7!=1:
            data=xml_file_name+" is Missing Thumbnail\n"
            #f.write(data)
            missing_fields.append(data)
        if r8!=1:
            data=xml_file_name+" is Missing High Res\n"
            #f.write(data)
            missing_fields.append(data)
        #server.sendmail("testintegrate2017@gmail.com", "michael.vanderlyn@verizondigitalmedia.com", msg)
        server.quit()
        return ['Invalid',missing_fields]
    return "Finished\n"








    V.validate(Doc,"cidentifier:Asset_Name_package").isNotMissing().matchesRegex("^.{1,50}$","Package Asset_Name should not be greater than 50 characters");
    V.validate(Doc, "cidentifier:Asset_ID_package").isNotMissing().matchesRegex("^[A-Z]{4}[0-9]{16}$","Package Asset_ID should have 4 alpha followed by 16 numbers");
    V.validate(Doc, "cprovider:Provider_Version_Major_package").matchesRegex("^\\d*$","Package Version Major should be a number");
    V.validate(Doc, "cprovider:Provider_Version_Minor_package").matchesRegex("^\\d*$","Package Version Minor should be a number");
    V.validate(Doc, "cfios:Product").isNotMissing().matchesRegex("^.{1,20}$","Product should not be greater than 20 characters");
    V.validate(Doc,"cidentifier:Asset_Name").isNotMissing().matchesRegex("^.{1,50}$","Title Asset_Name should not be greater than 50 characters");
    V.validate(Doc, "cprovider:Provider_Version_Major").isNotMissing().matchesRegex("^\\d*$","Title Version Major should be a number");
    V.validate(Doc, "cprovider:Provider_Version_Minor").isNotMissing().matchesRegex("^\\d*$","Title Version Minor should be a number");
    V.validate(Doc, "cidentifier:Asset_ID").isNotMissing().matchesRegex("^[A-Z]{4}[0-9]{16}$","Title Asset_ID should be 4 alpha followed by 16 numbers");
    V.validate(Doc, "ctitle:Title_Brief").isNotMissing().matchesRegex("^.{1,19}$","Title Brief should not be missing and should not exceed 19 chars");
    V.validate(Doc, "ctitle:Title").isNotMissing().matchesRegex("^.{1,128}$","Title should not be missing and should not exceed 128 chars");
    V.validate(Doc, "ctitle:Summary_Long").matchesRegex("^.{1,4096}$","Summary_Long should not exceed 4096 chars");
    V.validate(Doc, "ctitle:Summary_Short").isNotMissing().matchesRegex("^.{1,256}$","Summary_Short should not be missing and should not exceed 256 chars");
    V.validate(Doc, "ctitle:Year").isNotMissing().matchesRegex("^(19[0-9][0-9]|20[0-2]\\d|2030)$","Year should not be missing and should be between 1900 and 2030");
    V.validate(Doc, "ctitle:Genre").isNotEmptyMultiValuedList();
    V.validate(Doc, "ctitle:Studio").canBeMissing().matchesRegex("^.{1,32}$","Studio should not exceed 32 chars");
    V.validate(Doc, "ctitle:Show_type").isIn().items("series", "Sports", "Music", "Ad", "Miniseries","movie", "Game", "Other","Movie","Series");
    V.validate(Doc, "cidentifier:Content_type").isNotMissing();
    V.validate(Doc, "ctitle:Rating").isNotMissing().isIn().items("TV-Y","TV-Y7","TV-Y7-FV","TV-G","TV-PG","TV-14","TV-MA","TV-Unrated","G","PG","PG-13","R","NC-17","X","XX","XXX","NR","EC","E","E10+","T","M","AO","RP","M (17+)","TV14","TVMA");
    V.validate(Doc, "ctitle:Rating_Preview").canBeMissing().isIn().items("TV-Y","TV-Y7","TV-Y7-FV","TV-G","TV-PG","TV-14","TV-MA","TV-Unrated","G","PG","PG-13","R","NC-17","X","XX","XXX","NR","EC","E","E10+","T","M","AO","RP","M (17+)","TV14","TVMA");

    V.validate(Doc, "cfios:Box_Office").canBeMissing().matchesRegex("^\\d*$","Box_Office should be a number");
    V.validate(Doc, "cfios:Propagation_Priority").canBeMissing().matchesRegex("^([0-9]|[1-9]|10)$","Propagation_Priority should be a number");
    V.validate(Doc, "cidentifier:Billing_ID").matchesRegex("^.{5}$","Billing_ID should be of 5 digits");
    V.validate(Doc, "cfios:EST_Wholesale_Price").canBeMissing().matchesRegex("^\\d{1,5}[.]\\d{1,2}$","EST_Wholesale_Price should be of the form xx.yy");
    V.validate(Doc, "cfios:Rental_Price").canBeMissing().matchesRegex("^\\d{1,5}[.]\\d{1,2}$","Rental_Price should be of the form xx.yy");
    V.validate(Doc, "cfios:SD_Rental_Price").canBeMissing().matchesRegex("^\\d{1,5}[.]\\d{1,2}$");
    V.validate(Doc, "cfios:Rental_Window").canBeMissing().matchesRegex("^30$");
    V.validate(Doc, "cfios:Rental_Viewing_Window").canBeMissing().isIn().items("24","48","72");
    V.validate(Doc, "cfios:HD_Rental_Price").canBeMissing().matchesRegex("^\\d{1,5}[.]\\d{1,2}$");
    V.validate(Doc, "cfios:Distributor_Name").canBeMissing().matchesRegex("^.{1,128}$");
    V.validate(Doc,"cidentifier:Alt_Code").isNotMissing().matchesRegex("^[A-Z]{4}[0-9]{16}$");
    V.validate(Doc, "cidentifier:Description").isNotMissing().matchesRegex("^.{1,128}$");
    V.validate(Doc, "cidentifier:Description_package").isNotMissing().matchesRegex("^.{1,128}$");
    V.validate(Doc, "cvideo:Run_Time").matchesRegex("^([0-2][0-3]:[0-5][0-9])|(0?[0-9]:[0-5][0-9])$");
    V.validate(Doc, "cvideo:Run_Time_preview").canBeMissing().matchesRegex("^([0-2][0-3]:[0-5][0-9])|(0?[0-9]:[0-5][0-9])$");
    V.validate(Doc, "cfios:Display_As_Last_Chance").canBeMissing().matchesRegex("^\\d$");
    V.validate(Doc, "cfios:Display_As_New").canBeMissing().matchesRegex("^\\d$");

    V.validate(Doc, "cfios:Preview_Period").canBeMissing().matchesRegex("^\\d*$");
    V.validate(Doc, "cfios:Viewing_Can_Be_Resumed").canBeMissing().isIn().items("True", "False","true", "false");
    V.validate(Doc, "cfios:Provider_QA_Contact").canBeMissing().matchesRegex("[a-zA-Z0-9@._-]");
    V.validate(Doc, "cfios:Licensing_Window_End").dateTime();
    V.validate(Doc, "cfios:HD_Licensing_Window_End").canBeMissing().dateTime();
    V.validate(Doc, "cfios:Rental_Window_End").canBeMissing().dateTime();
    V.validate(Doc, "cfios:EST_Suggested_Price").canBeMissing().matchesRegex("^\\d{1,5}[.]\\d{1,2}$");
    V.validate(Doc,"cfios:Licensing_Window_End").isNotMissing().dateTime().after().field("cfios:Licensing_Window_Start",true);
    V.validate(Doc,"cfios:HD_Rental_Window_End").canBeMissing().dateTime().after().field("cfios:HD_Rental_Window_Start",true);
    V.validate(Doc,"cfios:Rental_Window_End").canBeMissing().dateTime().after().field("cfios:Rental_Window_Start",true);
    V.validate(Doc,"cfios:HD_Licensing_Window_End").canBeMissing().dateTime().after().field("cfios:HD_Licensing_Window_Start",true);
    V.validate(Doc, "cfios:HD_Licensing_Window_End").canBeMissing().dateTime().after().now();
    V.validate(Doc, "cfios:Licensing_Window_End").isNotMissing().dateTime().after().now();
    V.validate(Doc, "xcode:FIOS_SD_preview").isNotMissing();
    V.validate(Doc, "xcode:FIOS_SD_movie").isNotMissing();
    V.validate(Doc, "xcode:HLS_SM_SD_movie").isNotMissing();
    V.validate(Doc, "xcode:EM-iPHONE_preview").isNotMissing();
    V.validate(Doc, "xcode:EM-iPHONE_movie").isNotMissing();
    var pdt =   Doc.getPropertyValue("cfios:Product").toString();

    var hdpp = Doc.getPropertyValue("cfios:HD_Purchase_Price");
    if (pdt == "TVOD"  && hdpp !== null && hdpp.length>0) {
    	V.validate(Doc, "cfios:HD_Purchase_Window_Start").isNotMissing();
            V.validate(Doc, "cfios:HD_Purchase_Window_End").isNotMissing();
    }
    var hdrp = Doc.getPropertyValue("cfios:HD_Rental_Price");
    if (pdt == "TVOD" )
    {
       if (hdrp == "" || hdrp == null || hdrp == undefined) {}
    else
     {
       V.validate(Doc, "cfios:HD_Rental_Window_Start").isNotMissing();
        V.validate(Doc, "cfios:HD_Rental_Window_End").isNotMissing();
      }
    }

    var hdrws = Doc.getPropertyValue("cfios:HD_Rental_Window_Start");
    if ((pdt == "TVOD"  && hdrws !== null) ) {
    	V.validate(Doc, "cfios:HD_Rental_Price").isNotMissing();
            V.validate(Doc, "cfios:HD_Rental_Window_End").isNotMissing();
    }

    var sdpp = Doc.getPropertyValue("cfios:SD_Purchase_Price");
    if (pdt == "TVOD"  && sdpp !== null && sdpp.length>0) {
    	V.validate(Doc, "cfios:SD_Purchase_Window_Start").isNotMissing();
            V.validate(Doc, "cfios:SD_Purchase_Window_End").isNotMissing();
    }
    var sdrp = Doc.getPropertyValue("cfios:SD_Rental_Price");
    if (pdt == "TVOD"  && sdrp !== null && sdrp.length>0) {
    	V.validate(Doc, "cfios:SD_Rental_Window_Start").isNotMissing();
            V.validate(Doc, "cfios:SD_Rental_Window_End").isNotMissing();
    }
    var sdpws = Doc.getPropertyValue("cfios:SD_Purchase_Window_Start");
    if (pdt == "TVOD"  && sdpws !== null && sdpws.length>0) {
    	V.validate(Doc, "cfios:SD_Purchase_Price").isNotMissing();
            V.validate(Doc, "cfios:SD_Purchase_Window_End").isNotMissing();
    }
    var hdpws = Doc.getPropertyValue("cfios:HD_Purchase_Window_Start");
    if (pdt == "TVOD"  && hdpws !== null && hdpws.length>0) {
    	V.validate(Doc, "cfios:HD_Purchase_Price").isNotMissing();
            V.validate(Doc, "cfios:HD_Purchase_Window_End").isNotMissing();
    }
    V.validate(Doc, "cprovider:Provider_Content_Tier_package").canBeMissing().matchesRegex("^.{1,100}$");
    V.validate(Doc, "cfios:Platform_Streaming").canBeMissing().isIn().items("Y", "N");
    V.validate(Doc, "cfios:Platform_SVOD").canBeMissing().isIn().items("Y", "N");
    V.validate(Doc, "cprovider:Metadata_Spec_Version").canBeMissing().isIn().items("CableLabsVOD1.1");
    V.validate(Doc, "ctitle:Summary_Medium").canBeMissing().matchesRegex("^.{1,1024}$");
    V.validate(Doc, "cshared:Adult_Restricted").canBeMissing().isIn().items("Y", "N","true","false");
    V.validate(Doc, "ctitle:Animation").canBeMissing().isIn().items("Y", "N","null","false","true","n","y");
    var type = Doc.getPropertyValue("cidentifier:Content_type");
    if (type == "TVShow") {
    	V.validate(Doc, "cfios:Original_Air_Date").canBeMissing().dateTime().after().dateTime("1901-01-01");
            V.validate(Doc, "ctitle:Season_Premiere").canBeMissing().isIn().items("Y", "N");
    	V.validate(Doc, "ctitle:Season_Finale").canBeMissing().isIn().items("Y", "N");
            V.validate(Doc, "ctitle:Episode_ID").isNotMissing().matchesRegex("[a-zA-Z0-9_-]");
    	V.validate(Doc, "ctitle:Episode_Name").isNotMissing().matchesRegex("[a-zA-Z0-9&._-]");
    	V.validate(Doc, "ctitle:Episode_Number").isNotMissing().matchesRegex("[a-zA-Z0-9_-]");
    	V.validate(Doc, "ctitle:Season").isNotMissing().matchesRegex("^\\d*$");
    	V.validate(Doc, "ctitle:Series_Name").isNotMissing();
    }
    var type = Doc.getPropertyValue("cfios:Product");
    if (type == "SVOD" || type == "FVOD") {
    	V.validate(Doc, "cfios:Subscription_brand").isNotMissing();
            V.validate(Doc, "cfios:Subscription_type").isNotMissing();
            V.validate(Doc, "cfios:Subscription_Start_Date").canBeMissing().dateTime();
            V.validate(Doc, "cfios:Subscription_End_Date").canBeMissing().dateTime();
    }
    V.modify(Doc, "ctitle:Genre").map("genres");
    V.validate(Doc, "cidentifier:Provider").isIn().vocabulary("Provider");
    V.validate(Doc, "cidentifier:Provider_ID").isIn().vocabulary("ProviderID");
