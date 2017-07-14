
from xml.dom import minidom
import re
import os
import fnmatch
import string


#Function to Check for Class Attributes in the xml

class XmlContentValidator:

    def validateClass(self,xmlfilename):

        r=0
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

            print "Valid XML"


        else:

            print "Invalid XML"
            print "Error-Required Asset Classes missing"


        return "Done"






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

                    return "Valid Contents in the XML"

        else:
                    return "Invalid Contents in the XML"





#validateTVODXML('Lambert_StampTVNX0038260202255551SMOOTH_SD.xml')
#validateClass('Lambert_StampTVNX0038260202255551SMOOTH_SD.xml')
