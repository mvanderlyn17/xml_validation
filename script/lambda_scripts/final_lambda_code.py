#######################################################################################################
# Lambda script for internship project 2017                                                           #
# Programmed by: Michael Vanderlyn, Tyler Raffensperger, Saumya Shukla, Sairaj Alve                   #
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
import logging
###############################################<FUNCTIONS>############################################
def lambda_handler(event, context):
# Main function, called when a new xml is sent to the gen3-trigger bucket. When triggered information on
# the xml is sent to the function via a json being passed to the event parameter, and the filename and bucket
# are extracted from the event json. Then the xml is either validated with viacom or nbc validation scripts
# after this if its validated its moved to the validated bucket for its content provider, otherwise its
# moved to a seperate bucket for failed xmls for that content provider, and emails are sent out to notify
# our team and the content provider
    start_time = datetime.now()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info('got event{}'.format(event))
    global f
    s3_client = boto3.client('s3')
    logger.info('hello there')
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key'].replace("+"," ")
        #print(key)
        #print(str(key))
        if "%26" in key:
            key =key.replace("%26","&")
        print("bucket: "+bucket)
        print("key: "+key)
        response = s3_client.get_object(Bucket=bucket, Key=key)
        print("got: "+str(response));
        s3_client.delete_object(Bucket=bucket, Key=key)
        file_content = response['Body'].read().decode('utf-8')
        xml_file = minidom.parseString(file_content)
        itemlist = xml_file.getElementsByTagName('App_Data')
        if(itemlist):
            s =itemlist[0]
            content_provider=(s.attributes['Value'].value)
        else:
            content_provider = ''
        fnselector = 0
        output = None
        if(content_provider == 'nbcuniversal') or (content_provider=='MSV_4K_NBCU'):
            content_provider = 'nbcuniversal';
            output = validateNBC(xml_file, key)
        else:
            content_provider = 'viacom'
            output = validateViacom(xml_file, key)
        if not(output ==None):
            package_name = key.replace(".xml","")
            package_name = package_name.replace("in/", "")
            validity_status = output[0]
            invalid_fields = output[1]
            if(len(invalid_fields)<=0):
                invalid_fields = "[]"
            else:
                invalid_fields = '; '.join(invalid_fields)
            f = open('/tmp/'+package_name+'_logs.txt', 'w')
            f.write('content_provider,package_name,validity_status,invalid_fields\n'+content_provider+","+package_name+","+validity_status+","+invalid_fields)
            f.close()
            print('Filename: '+package_name)
            if(validity_status =="Valid"):
                logger.error("Valid")
                #print('Status: Valid')
                ###check if file is already in invalid, and delete it
                try:
                    s3_client.delete_object(Bucket='gen3-interns-trigger', Key='invalid'+package_name+'_logs.txt')
                    s3_client.upload_file('/tmp/'+package_name+'_logs.txt', 'gen3-interns-trigger', 'valid/'+package_name+'_logs.txt')
                except:
                    s3_client.upload_file('/tmp/'+package_name+'_logs.txt', 'gen3-interns-trigger', 'valid/'+package_name+'_logs.txt')
            else:
                #print('Status: Invalid')
                logger.error("Invalid")
                s3_client.upload_file('/tmp/'+package_name+'_logs.txt', 'gen3-interns-trigger', 'invalid/'+package_name+'_logs.txt')
            logger.info('Content Provider: '+content_provider)
            logger.info('Invalid Fields: '+invalid_fields)
            #print('Content Provider: '+content_provider)
            #print('Invalid Fields: '+invalid_fields)
        else:
            print("Validation failed- ERROR IN CODE")

def validateViacom(xml_file, xmlfilename):
# Validates XMLS based off the scheme for the content provider Viacom. Takes in the content of an xml for
# xml_file, and the name of the file for xmlfilename
    t1=t2=t3=t4=t5=t6=t7=t8=t9=t10=t11=t12=t13=t14=t15=t16=t17=t18=t19=0
    xmlfilename = xmlfilename.replace("in/","")
    package = xml_file.getElementsByTagName('package')
    if(package == []):
        missing_fields = []

        data = xmlfilename + ' is Missing Package; or Content Provider Not Supported'
        missing_fields.append(data)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("testintegrate2017@gmail.com", "Terminator90!")

        email =  str('\n'.join([str(x) for x in missing_fields]))
        server.sendmail("testintegrate2017@gmail.com", "ty.raffensperger@gmail.com", email)
        server.quit()
        del missing_fields[0]
        return ['Invalid',missing_fields]

    for node in package:
        packVersion=node.getAttribute('version')
        if packVersion !="":
            t1=1
    itemlist = xml_file.getElementsByTagName('video')
    for node in itemlist:
        alist=node.getElementsByTagName('video_type')
        for a in alist:
            videoType= a.childNodes[0].nodeValue
            if videoType=="TV" or videoType=="film":
                t2=1
        clist = node.getElementsByTagName('network_name')
        for c in clist:
            networkName = c.childNodes[0].nodeValue
            if len(networkName)!=0:
                t3=1
        dlist=node.getElementsByTagName('unique_id_series')
        for d in dlist:
            uniqueidSeries = d.childNodes[0].nodeValue
            if len(uniqueidSeries)!=0:
                t4=1
        elist = node.getElementsByTagName('unique_id_season')
        for e in elist:
            uniqueidSeason = e.childNodes[0].nodeValue
            if len(uniqueidSeason)!= 0:
                t5 = 1
        flist = node.getElementsByTagName('unique_id_episode')
        for f in flist:
            uniqueidEpisode = f.childNodes[0].nodeValue
            if len(uniqueidEpisode)!= 0:
                t6 = 1
        glist= node.getElementsByTagName('episode_production_number')
        for g in glist:
            episodeprodNumber = g.childNodes[0].nodeValue
            if episodeprodNumber.isdigit():
                t7=1
        hlist=node.getElementsByTagName('show_type')
        for h in hlist:
            showType=h.childNodes[0].nodeValue
            #print('HO')
            if len(showType)!=0:
                t8=1
        ilist = node.getElementsByTagName('season_number')
        for i in ilist:
            seasonNumber = i.childNodes[0].nodeValue
            if seasonNumber.isdigit():
                t9 = 1
        jlist = node.getElementsByTagName('release_date')
        for j in jlist:
            try:
                releaseDate = j.childNodes[0].nodeValue
                valid_date = datetime.strptime(releaseDate, '%Y-%m-%d').date()
                t10=1
            except:
                pass
        klist=node.getElementsByTagName('original_release_year')
        for k in klist:
            origreleaseYear=k.childNodes[0].nodeValue
            if len(origreleaseYear)==4:
                t11=1
        blist = node.getElementsByTagName('genres')
        for b in blist:
            blistin = b.getElementsByTagName('genre')
            for bi in blistin:
                genree = bi.childNodes[0].nodeValue
            try:
                if len(genree)!=0:
                    t12=1
            except (IndexError,ValueError):
                    pass
        llist = node.getElementsByTagName('video_file')
        for l in llist:
            llistin = l.getElementsByTagName('file_name')
            for li in llistin:
                fileName1 = li.childNodes[0].nodeValue
                if fileName1.endswith('mpg'):
                    t13=1
        mlist = node.getElementsByTagName('captions')
        for m in mlist:
            mlistin = m.getElementsByTagName('file_name')
            for mi in mlistin:

                fileName2 = mi.childNodes[0].nodeValue
                if fileName2.endswith('scc'):#changd scc to SCC
                    t14 = 1
        nlist = node.getElementsByTagName('image')
        for n in nlist:
            nlistin = n.getElementsByTagName('file_name')
            for ni in nlistin:
                fileName3 = ni.childNodes[0].nodeValue
                if fileName3.endswith('jpg'):
                    t15 = 1
        olist = node.getElementsByTagName('sales_start_date')
        for o in olist:
            salesstartDate = o.childNodes[0].nodeValue
            try:
                valid_date1 = datetime.strptime(salesstartDate, '%Y-%m-%d').date()
                t16 = 1
            except:
                pass
        plist = node.getElementsByTagName('episode_short_description')
        for p in plist:
            episodeshortdescrip = p.childNodes[0].nodeValue
            if (len(episodeshortdescrip)<256):
                t17=1
        qlist = node.getElementsByTagName('episode_long_description')
        for q in qlist:
            episodelongdescrip = q.childNodes[0].nodeValue
            if (len(episodelongdescrip) < 1024):
                t18 = 1
        if( t1==t2==t3==t4==t5==t6==t7==t8==t9==t10==t11==t12==t13==t14==t15==t16==t17==t18==1):
            #server = smtplib.SMTP('smtp.gmail.com', 587)
            #server.starttls()
            #server.login("testintegrate2017@gmail.com", "Terminator90!")
            #msg = 'File is valid!'
            #server.sendmail("testintegrate2017@gmail.com", "ty.raffensperger@gmail.com", msg)
            #server.quit()
            return ["Valid", []]
        else:
            missing_fields = []
            print(t1)
            print(t2)
            print(t3)
            print(t4)
            print(t5)
            print(t6)
            print(t7)
            print(t8)
            print(t9)
            print(t10)
            print(t11)
            print(t12)
            print(t13)
            print(t14)
            print(t15)
            print(t16)
            print(t17)
            print(t18)
            if t1 != 1:
                data = xmlfilename + ' is Missing Package Version'
                missing_fields.append(data)
            if t2 != 1:
                data = xmlfilename + ' has Invalid Video Type'
                missing_fields.append(data)
            if t3 != 1:
                data = xmlfilename + ' is Missing Network name'
                missing_fields.append(data)
            if t4 != 1:
                data = xmlfilename + ' is Missing Series ID'
                missing_fields.append(data)
            if t5 != 1:
                data = xmlfilename + ' is Missing Season ID'
                missing_fields.append(data)
            if t6 != 1:
                data = xmlfilename + ' is Missing Episode ID'
                missing_fields.append(data)
            if t7 != 1:
                data = xmlfilename + ' is Not Numeric'
                missing_fields.append(data)
            if t8 != 1:
                data = xmlfilename + ' is Missing Show Type'
                missing_fields.append(data)
                #print(str(missing_fields))
            if t9 != 1:
                data = xmlfilename + ' has a Non-Numerical Season Number'
                missing_fields.append(data)
            if t10 != 1:
                data = xmlfilename + ' has Invalid Date Format'
                missing_fields.append(data)
            if t11 != 1:
                data = xmlfilename + ' is Missing Valid Year Format'
                missing_fields.append(data)
            if t12 != 1:
                data = xmlfilename + ' Does Not Have Genre' #mp4 suffix
                missing_fields.append(data)
            if t13 != 1:
                data = xmlfilename + ' Does Not Have mpg Suffix' #scc suffix
                missing_fields.append(data)
            if t14 != 1:
                data = xmlfilename + ' Does Not Have .SCC Suffix' #valid year format
                missing_fields.append(data)
            if t15 != 1:
                data = xmlfilename + ' Does Not Have .Jpg Suffix'
                missing_fields.append(data)
            if t16 != 1:
                data = xmlfilename + ' Does Not Have Correct Date Format'
                missing_fields.append(data)
            if t17 != 1:
                data = xmlfilename + ' Exceeds 256 Characters'
                missing_fields.append(data)
            if t18 != 1:
                data = xmlfilename + ' Exceeds 1024 Characters'
                missing_fields.append(data)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("testintegrate2017@gmail.com", "Terminator90!")
        email =  str('\n'.join([str(x) for x in missing_fields]))
        server.sendmail("testintegrate2017@gmail.com", "ty.raffensperger@gmail.com", email)
        server.quit()
    return ['Invalid',missing_fields]









def validateNBC(xml_file, xml_file_name):
# Validates XMLS based off the scheme for the content provider NBC. Takes in the content of an xml for
# xml_file, and the name of the file for xml_file_name
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("testintegrate2017@gmail.com", "Terminator90!")
    validity_check= []
    missing_fields=[]
    data = " "
    check1=check2=check3=correct=check_val=r=r1=r2=r3=r4=r5=r6=r7=r8=0
    xml_file_name = xml_file_name.replace("in/","")
    xml_file_name = xml_file_name.replace(".xml","")
    value1=value2=""
    itemlist = xml_file.getElementsByTagName('AMS')
    for s in itemlist:
        try:
            values=(""+s.attributes['Asset_Class'].value).lower()
        except:
            values = ""
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
    if r1==1 and r2==1 and r3==1 and r4==1:
        #msg = 'File is valid!'
        #server.sendmail("testintegrate2017@gmail.com", "ty.raffensperger@gmail.com", msg)
        #server.quit()
        return ["Valid",[]]
    else:
        if r1!=1:
            data=xml_file_name + " is Missing Package Name"
            missing_fields.append(data)
            validity_check.append("Invalid")
        if r2!=1:
            data=xml_file_name + " is Missing Title"
            missing_fields.append(data)
            validity_check.append("Invalid")
        if r3!=1:
            data=xml_file_name + " is Missing Movie"
            missing_fields.append(data)
            validity_check.append("Invalid")
        if r4!=1:
            data=xml_file_name + " is Missing Preview"
            missing_fields.append(data)
            validity_check.append("Invalid")
        if r5!=1:
            data=xml_file_name + " is Missing Poster"
            validity_check.append("Invalid")
            missing_fields.append(data)
        if r6!=1:
            data=xml_file_name + " is Missing Box Cover"
            missing_fields.append(data)
            validity_check.append("Invalid")
        if r7!=1:
            data=xml_file_name + " is Missing Thumbnail"
            missing_fields.append(data)
            validity_check.append("Invalid")
        if r8!=1:
            data=xml_file_name + " is Missing High Res"
            missing_fields.append(data)
            validity_check.append("Invalid")
    itemlist1 = xml_file.getElementsByTagName('AMS')
    for s in itemlist1:
        values=(s.attributes['Provider_ID'].value)
        if(values==" "):
            missing_fields.append("Provider ID is missing")
            validity_check.append("Invalid")
        else:
            validity_check.append("Valid")
    itemlist2=xml_file.getElementsByTagName('App_Data')
    for s in itemlist2:
        value1=(s.attributes["Name"].value)
        value2=(s.attributes["Value"].value)
        if(value1=="Is4K"):
            if(value2=="Y" or value2=="N"):
                correct=10
            else:
                check2=1
        else:
            check1=1
    if correct==10:
        validity_check.append("Valid")
    else:
        if check1==1 or check2==1:
            missing_fields.append("Is4k is missing or Value for Is4k tag is not Y or N")
            validity_check.append("Invalid")
    itemlist3 = xml_file.getElementsByTagName('App_Data')
    for s in itemlist3:
        value1 = (s.attributes["Name"].value)
        value2 = (s.attributes["Value"].value)
        if(value1=="Type"):
            if(value2=="title"):
                correct=10
            else:
                check2=1
        else:
            check1=1
    if correct==10:
        validity_check.append("Valid")
    else:
        if check1==1 or check2==1:
            validity_check.append("Invalid")
            missing_fields.append("Type  is missing or Type title is missing")
    itemlist3 = xml_file.getElementsByTagName('App_Data')
    for s in itemlist3:
        value1 = (s.attributes["Name"].value)
        value2 = (s.attributes["Value"].value)
        if(value1=="Title_Brief"):
            if(value2==" " or len(value2)>19):
                    check2=1
            else:
                correct=10
        else:
            check1=1
    if correct==10:
        validity_check.append("Valid")
    else:
        if check1 == 1 or check2==1:
            validity_check.append("Invalid")
            missing_fields.append("Title_Brief is missing or Title_Brief value is greater than 19 characters")
    itemlist3 = xml_file.getElementsByTagName('App_Data')
    for s in itemlist3:
        value1 = (s.attributes["Name"].value)
        value2 = (s.attributes["Value"].value)
        if (value1 == "Title"):
            if (value2 == " "):
                check2=1
            else:
                correct=10
        else:
            check1=1
    if correct == 10:
        validity_check.append("Valid")
    else:
        if check1 == 1 or check2 == 1:
            validity_check.append("Invalid")
            missing_fields.append("Title is missing or Title value is missing ")
    itemlist3 = xml_file.getElementsByTagName('App_Data')
    for s in itemlist3:
        value1 = (s.attributes["Name"].value)
        value2 = (s.attributes["Value"].value)
        if (value1 == "Summary_Short"):
            if (len(value2)>256):
                check2=1
            else:
                correct=10
        else:
            check1=1
    if correct==10:
        validity_check.append("Valid")
    else:
        if check1 == 1 or check2==1:
            validity_check.append("Invalid")
            missing_fields.append("Summary_Short is missing or Summary_Short length is greater than 256 characters")
    itemlist3 = xml_file.getElementsByTagName('App_Data')
    for s in itemlist3:
        value1 = (s.attributes["Name"].value)
        value2 = (s.attributes["Value"].value)
        if (value1 == "Summary_Long"):
            if (len(value2)>1024):
                check2=1
            else:
                correct=10
        else:
            check1=1
    if correct==10:
        validity_check.append("Valid")
    else:
        if check1 == 1 or check2==1:
            validity_check.append("Invalid")
            missing_fields.append("Summary_Long is missing or Summary_Short length is greater than 1024 characters")
    itemlist3 = xml_file.getElementsByTagName('App_Data')
    for s in itemlist3:
        value1 = (s.attributes["Name"].value)
        value2 = (s.attributes["Value"].value)
        if (value1 == "Billing_ID"):
            if (len(value2)>5):
                check2=1
            else:
                correct=10
        else:
            check1=1
    if correct==10:
        validity_check.append("Valid")
    else:
        if check1 == 1 or check2==1:
            validity_check.append("Invalid")
            missing_fields.append("Billing_ID is missing or Billing_ID length is greater than 5 characters")
    itemlist3 = xml_file.getElementsByTagName('App_Data')
    for s in itemlist3:
        value1 = (s.attributes["Name"].value)
        value2 = (s.attributes["Value"].value)
        if (value1 == "Rating"):
            if (value2==" "):
                check2=1
            else:
                correct=10
        else:
            check1=1
    if correct==10:
        validity_check.append("Valid")
    else:
        if check1 == 1 or check2==1:
            validity_check.append("Invalid")
            missing_fields.append("Rating field is missing or Rating value is missing")
    itemlist3 = xml_file.getElementsByTagName('App_Data')
    for s in itemlist3:
        value1 = (s.attributes["Name"].value)
        value2 = (s.attributes["Value"].value)
        if (value1 == "Genre"):
            if (len(value2)>3):
                correct=10
            else:
                check2=1
        else:
                check1=1
    if correct==10:
        validity_check.append("Valid")
    else:
        if check1 == 1 or check2 ==1:
            validity_check.append("Invalid")
            missing_fields.append("Genre is missing or Genre value length is less than 3 characters")
    itemlist3 = xml_file.getElementsByTagName('App_Data')
    for s in itemlist3:
        value1 = (s.attributes["Name"].value)
        value2 = (s.attributes["Value"].value)
        if (value1 == "Category"):
            if (len(value2)>3):
                correct=10
            else:
                check2=1
        else:
            check1=1
    if correct==10:
        validity_check.append("Valid")
    else:
        if check1 == 1 or check2==1:
            validity_check.append("Invalid")
            missing_fields.append("Category is missing or Category value length is less than 3 characters")
    itemlist3 = xml_file.getElementsByTagName('App_Data')
    for s in itemlist3:
        value1 = (s.attributes["Name"].value)
        value2 = (s.attributes["Value"].value)
        if (value1 == "Licensing_Window_Start"):
            if (value2==" "):
                check2=1
            else:
                correct=10
        else:
            check1=1
    if correct==10:
        validity_check.append("Valid")
    else:
        if check1 == 1 or check2==1:
            validity_check.append("Invalid")
            validity_check.append("Licensing_Window_Start is missing or License_Window_Start value is missing")
    itemlist3 = xml_file.getElementsByTagName('App_Data')
    for s in itemlist3:
        value1 = (s.attributes["Name"].value)
        value2 = (s.attributes["Value"].value)
        if(value1=="4K_SDR_VideoFile"):
            if(value2!=" "):
                temp=value2
    itemlist3 = xml_file.getElementsByTagName('App_Data')
    for s in itemlist3:
        value1 = (s.attributes["Name"].value)
        value2 = (s.attributes["Value"].value)
        if (value1 == "4K_HDR_VideoFile"):
            if (value2 != " "):
                temp = value2
    itemlist3 = xml_file.getElementsByTagName('App_Data')
    for s in itemlist3:
        value1 = (s.attributes["Name"].value)
        value2 = (s.attributes["Value"].value)
        if(value1=="4K_SCCFile"):
            validity_check.append("Valid")
            correct=10
            if(value2!=" "):
                validity_check.append("Valid")
                correct=11
                if(".scc" in value2):
                    validity_check.append("Valid")
                    correct=12
                else:
                    check3=1
            else:
                check2 = 1
        else:
            check1 = 1
    if correct==12:
        validity_check.append("Valid")
    else:
        if check1 == 1 or check2==1 or check3==1:
            validity_check.append("Invalid")
            missing_fields.append("No 4K Scc file or No sub captions or SCC file does not have .scc extension ")
    itemlist3 = xml_file.getElementsByTagName('App_Data')
    for s in itemlist3:
        value1 = (s.attributes["Name"].value)
        value2 = (s.attributes["Value"].value)
        if(value1=="AdBreak"):
            correct=10
        else:
            check1=1
    if correct==10:
        validity_check.append("Valid")
    else:
        if check1 == 1:
            validity_check.append("Invalid")
            missing_fields.append("AdBreak not available")
    for i in range(len(validity_check)):
        if validity_check[i]=='Invalid':
            check_val=check_val+1
    if check_val>0:
        email =  str('\n'.join([str(x) for x in missing_fields]))
        server.sendmail("testintegrate2017@gmail.com", "ty.raffensperger@gmail.com", email)
        server.quit()
        return ['Invalid',missing_fields]
    else:
        #msg = 'File is valid!'
        #server.sendmail("testintegrate2017@gmail.com", "ty.raffensperger@gmail.com", msg)
        #server.quit()
        return ["Valid",[]]
