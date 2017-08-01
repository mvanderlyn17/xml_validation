from xml.dom import minidom



class nbcDemo:



    def nbcCheck(xmlfilename):


        validity_check=[]
        missing_fields=[]

        check2=0
        check1=0
        check3=0
        correct=0
        check_val=0

        wfile = open("Demo.txt", "a+")
        data = " "

        r = 0
        r1 = 0
        r2 = 0
        r3 = 0
        r4 = 0
        r5 = 0
        r6 = 0
        r7 = 0
        r8 = 0

        value1=""
        value2=""
        xmldoc = minidom.parse(xmlfilename)
        itemlist = xmldoc.getElementsByTagName('AMS')


        for s in itemlist:

            values=(s.attributes['Asset_Class'].value)

            print values

            if values.lower()=="package":

                r1=1

            elif values.lower()=="title":

                r2=1

            elif values.lower()=="movie":

                r3=1

            elif values.lower()=="preview":

                r4=1

            elif values.lower()=="poster":

                r5=1

            elif values.lower()=="box cover":

                r6=1

            elif values.lower()=="thumb nail":

                r7=1

            elif values.lower()=="high res":

                r8=1

            else:
                continue


        if r1==1 and r2==1 and r3==1 and r4==1:

                wfile.write("Valid")


        else:

                if r1!=1:
                    data=xmlfilename + " is Missing Package\n\n"
                    missing_fields.append(data)
                    validity_check.append("Invalid")
                    wfile.write(data)

                if r2!=1:
                    data=xmlfilename + " is Missing Title\n\n"
                    missing_fields.append(data)
                    validity_check.append("Invalid")

                    wfile.write(data)


                if r3!=1:
                    data=xmlfilename + " is Missing Movie\n\n"
                    missing_fields.append(data)
                    validity_check.append("Invalid")

                    wfile.write(data)


                if r4!=1:
                    data=xmlfilename + " is Missing Preview\n\n"
                    missing_fields.append(data)
                    validity_check.append("Invalid")

                    wfile.write(data)


                if r5!=1:
                    data=xmlfilename + " is Missing Poster\n\n"
                    validity_check.append("Invalid")
                    missing_fields.append(data)

                    wfile.write(data)


                if r6!=1:
                    data=xmlfilename + " is Missing Box Cover\n\n"
                    missing_fields.append(data)
                    validity_check.append("Invalid")

                    wfile.write(data)


                if r7!=1:
                    data=xmlfilename + " is Missing Thumbnail\n\n"
                    missing_fields.append(data)
                    validity_check.append("Invalid")

                    wfile.write(data)


                if r8!=1:
                    data=xmlfilename + " is Missing High Res\n\n"
                    missing_fields.append(data)
                    validity_check.append("Invalid")

                    wfile.write(data)




        itemlist1 = xmldoc.getElementsByTagName('AMS')


        for s in itemlist1:


            values=(s.attributes['Provider_ID'].value)


            if(values==" "):

                missing_fields.append("Provider ID is missing")
                validity_check.append("Invalid")


            else:

                validity_check.append("Valid")



        itemlist2=xmldoc.getElementsByTagName('App_Data')


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





        itemlist3 = xmldoc.getElementsByTagName('App_Data')

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




        itemlist3 = xmldoc.getElementsByTagName('App_Data')

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




        itemlist3 = xmldoc.getElementsByTagName('App_Data')

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




        itemlist3 = xmldoc.getElementsByTagName('App_Data')

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




        itemlist3 = xmldoc.getElementsByTagName('App_Data')

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





        itemlist3 = xmldoc.getElementsByTagName('App_Data')


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




        itemlist3 = xmldoc.getElementsByTagName('App_Data')

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




        itemlist3 = xmldoc.getElementsByTagName('App_Data')

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



        itemlist3 = xmldoc.getElementsByTagName('App_Data')

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




        itemlist3 = xmldoc.getElementsByTagName('App_Data')

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




        itemlist3 = xmldoc.getElementsByTagName('App_Data')

        for s in itemlist3:
            value1 = (s.attributes["Name"].value)
            value2 = (s.attributes["Value"].value)

            if(value1=="4K_SDR_VideoFile"):

                if(value2!=" "):

                    temp=value2




        itemlist3 = xmldoc.getElementsByTagName('App_Data')

        for s in itemlist3:
            value1 = (s.attributes["Name"].value)
            value2 = (s.attributes["Value"].value)

            if (value1 == "4K_HDR_VideoFile"):

                if (value2 != " "):

                    temp = value2




        itemlist3 = xmldoc.getElementsByTagName('App_Data')

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





        itemlist3 = xmldoc.getElementsByTagName('App_Data')

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

            print "Invalid XML"


        else:

            print "Valid XML"


        print missing_fields



    nbcCheck("/Users/salve/PycharmProjects/Intern_Project/Mummy Returns_U5542_VZ_R.xml")