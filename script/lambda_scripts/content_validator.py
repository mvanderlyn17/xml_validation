
from xml.dom import minidom
import re
import os
import fnmatch
import string


#Function to Check for Class Attributes in the xml

class XmlContentValidator:

    def validateClass(self,xmlfilename):

        wfile=open("Demo.txt","a+")
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
        xmldoc = minidom.parse(xmlfilename)
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
                    wfile.write(data)
                    return "Invalid"

                if r2!=1:
                    data=xmlfilename+" is Missing Title\n\n"
                    wfile.write(data)
                    return "Invalid"


                if r3!=1:
                    data=xmlfilename+" is Missing Movie\n\n"
                    wfile.write(data)
                    return "Invalid"


                if r4!=1:
                    data=xmlfilename+" is Missing Preview\n\n"
                    wfile.write(data)
                    return "Invalid"


                if r5!=1:
                    data=xmlfilename+" is Missing Poster\n\n"
                    wfile.write(data)
                    return "Invalid"


                if r6!=1:
                    data=xmlfilename+" is Missing Box Cover\n\n"
                    wfile.write(data)
                    return "Invalid"


                if r7!=1:
                    data=xmlfilename+" is Missing Thumbnail\n\n"
                    wfile.write(data)
                    return "Invalid"


                if r8!=1:
                    data=xmlfilename+" is Missing High Res\n\n"
                    wfile.write(data)
                    return "Invalid"










    def validateTVODXML(self,xmlfile):

        pcheck=0
        pcheck2=0
        value1=0
        value2=0
        check2=0
        check=0
        check4=0
        check3=0
        check5=0
        check6=0


        xmldoc = minidom.parse(xmlfile)
        itemlist = xmldoc.getElementsByTagName('App_Data')


        format=xmlfile.split("TVNX",1)[0]

        format2=xmlfile.split("TVNX",1)[1]

        format3=format2[:16]

        pattern1=format+"*"+format3+"*SMOOTH_SD.xml"
        pattern2=format+"SMOOTH_HD.xml"
        pattern3=format+"FIOS_SD.xml"
        pattern4=format+"FIOS_HD.xml"
        pattern5=format+"IPTV_PKG.xml"



    #files=os.listdir('/Users/salve/Documents/Test3')

    #for name in files:

     #if fnmatch.fnmatch(name,pattern1):

        for s in itemlist:

            value1=(s.attributes['Name'].value)
            value2=(s.attributes['Value'].value)


            if (value1=="Rental_Price"):

                check=1

            else:

                continue


            if (value2 != " " or value2 == "0.00"):

                check2=1

            else:

                continue


        for s in itemlist:

            value1 = (s.attributes['Name'].value)
            value2 = (s.attributes['Value'].value)

            if (value1 == "Purchase_Price"):

                pcheck = 1

            else:

                continue

            if (value2 != " " or value2 == "0.00"):

                pcheck2 = 1

            else:

                continue


        for s in itemlist:

            value1 = (s.attributes['Name'].value)
            value2 = (s.attributes['Value'].value)


            if(pcheck==1 and pcheck2==1):

                if(value1=="Purchase" and value2=="Y"):

                    check3=1
            else:

                if(value1=="Purchase" and value2=="N"):
                    check3=2



            if(check==1 and check2==1):

                if (value1 == "Rental" and value2 == "Y"):

                    check4 = 1

            else:

                if(value1=="Rental" and value2=="N"):

                    check4=2


        for s in itemlist:

            value1 = (s.attributes['Name'].value)
            value2 = (s.attributes['Value'].value)


            if (check3==1 and check4==1):

                if(value1=="IsFreeVOD" and value2=="N"):

                    check5 = 1

                if(value1=="IsSubscription" and value2=="N"):

                    check6 = 1

            else:

                if (value1 == "IsFreeVOD" and value2 == "Y"):
                    check5 = 2

                if (value1 == "IsSubscription" and value2 == "Y"):
                    check6 = 2


        if ((check3 == 1 and check4 == 1 and check5 == 1 and check6 == 1) or (check5 == 1 and check6 == 1 and check5 == 2 and check6 == 2)):

                    return "Valid"

        else:
                    return "Invalid"





    # test1=validateTVODXML('Wind2016010601TVNX0039192016010602SMOOTH_SD.xml')
    # test2=validateClass('Wind2016010601TVNX0039192016010602SMOOTH_SD.xml')
    #
    #
    # print test1
    # print test2





    '''
def validateViacom(xml_file, xml_file_name):
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
        if values=="title":
            r2=1
        if values=="movie":
            r3=1
        if values=="preview":
            r4=1
        if values=="poster":
            r5=1
        if values=="box cover":
            r6=1
        if values=="thumb nail":
            r7=1
        if values=="high res":
            r8=1

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






    '''
