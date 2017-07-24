
def validateViacom(xmldoc, xml_doc_name):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("testintegrate2017@gmail.com", "Terminator90!")
    s3_client = boto3.client('s3')

    #xmldoc = minidom.parse('C:\\Users\\sshukla\\Desktop\\AWS Lambda\\Paramount.xml')
    t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16 = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
    package = xmldoc.getElementsByTagName('package')
    for node in package:
        packVersion=node.getAttribute('version')
        if packVersion !="":
            t1=1
            #print (t1)
            #print (t1)
        #print(packVersion)

    itemlist = xmldoc.getElementsByTagName('video')
    for node in itemlist:
        alist=node.getElementsByTagName('video_type')
        for a in alist:
            videoType= a.childNodes[0].nodeValue
            if videoType=="TV" or videoType=="film":
                t2=1
                #print(videoType)
        clist = node.getElementsByTagName('network_name')
        for c in clist:
            networkName = c.childNodes[0].nodeValue
            if len(networkName)!=0:
                t3=1
                #print(networkName)
                #print(len(networkName))
        dlist=node.getElementsByTagName('unique_id_series')
        for d in dlist:
            uniqueidSeries = d.childNodes[0].nodeValue
            if len(uniqueidSeries)!=0:
                t4=1
                #print(uniqueidSeries)
        elist = node.getElementsByTagName('unique_id_season')
        for e in elist:
            uniqueidSeason = e.childNodes[0].nodeValue
            if len(uniqueidSeason)!= 0:
                t5 = 1
                #print(uniqueidSeason)
        flist = node.getElementsByTagName('unique_id_episode')
        for f in flist:
            uniqueidEpisode = f.childNodes[0].nodeValue
            if len(uniqueidEpisode)!= 0:
                t6 = 1
                #print(uniqueidEpisode)
        glist= node.getElementsByTagName('episode_production_number')
        for g in glist:
            episodeprodNumber = g.childNodes[0].nodeValue
            if episodeprodNumber.isdigit():
                t7=1
                #print(episodeprodNumber)
        hlist=node.getElementsByTagName('show_type')
        for h in hlist:
            showType=h.childNodes[0].nodeValue
            if len(showType)!=0:
                t8=1
                #print(showType)
        ilist = node.getElementsByTagName('season_number')
        for i in ilist:
            seasonNumber = i.childNodes[0].nodeValue
            if seasonNumber.isdigit():
                t9 = 1
                #print(seasonNumber)
        jlist = node.getElementsByTagName('release_date')
        for j in jlist:
            releaseDate = j.childNodes[0].nodeValue
            try:
                valid_date = datetime.strptime(releaseDate, '%Y-%m-%d').date()
                t10=1
                #print(releaseDate)
            except:
                print('Invalid date')
        klist=node.getElementsByTagName('original_release_year')
        for k in klist:
            origreleaseYear=k.childNodes[0].nodeValue
            if len(origreleaseYear)==4:
                t11=1
                #print(origreleaseYear)

        blist = node.getElementsByTagName('genres')
        for b in blist:
            blistin = b.getElementsByTagName('genre')
            for bi in blistin:
                genree = bi.childNodes[0].nodeValue
            try:
                if len(genree)!=0:
                    t12=1
                    #print(genree)
            except (IndexError,ValueError):
                    pass
                    print('invalid')

        llist = node.getElementsByTagName('video_file')
        for l in llist:
            llistin = l.getElementsByTagName('file_name')
            for li in llistin:
                fileName1 = li.childNodes[0].nodeValue
                if fileName1.endswith('mp4'):
                    t13=1
                    #print(fileName1)
        mlist = node.getElementsByTagName('captions')
        for m in mlist:
            mlistin = m.getElementsByTagName('file_name')
            for mi in mlistin:
                fileName2 = mi.childNodes[0].nodeValue
                if fileName2.endswith('scc'):
                    t14 = 1
                    #print(fileName2)
        nlist = node.getElementsByTagName('image')
        for n in nlist:
            nlistin = n.getElementsByTagName('file_name')
            for ni in nlistin:
                fileName3 = ni.childNodes[0].nodeValue
                if fileName3.endswith('jpg'):
                    t15 = 1
                    #print(fileName3)
        olist = node.getElementsByTagName('sales_start_date')
        for o in olist:
            salesstartDate = o.childNodes[0].nodeValue
            try:
                valid_date1 = datetime.strptime(salesstartDate, '%Y-%m-%d').date()
                t16 = 1
                #print(salesstartDate)
            except:
                print('Invalid date')

        if t1==1 and t2==1 and t3==1 and t4==1 and t5==1 and t6==1 and t7==1 and t8==1 and t9==1 and t10==1 and t11==1 and t12==1 and t13==1 and t14==1 and t15==1 and t16==1:
            print('xml is valid')
            msg = 'File is valid!'
            server.sendmail("testintegrate2017@gmail.com", "michael.vanderlyn@verizondigitalmedia.com", msg)
            server.quit()
            return ["Valid",[]]
        else:
            missing_fields = []
            missing_fields.append('The XML you sent us is invalid for the following reason(s)..  \n\n ')
            if t1!=1:
                data=xml_file_name+" is Missing Package Version" #asset class missing
                missing_fields.append(data)
            if t2!=1:
                data=xml_file_name+" is Missing Video Type"
                missing_fields.append(data)
            if t3!=1:
                data=xml_file_name+" is Missing Network Name"
                missing_fields.append(data)
            if t4!=1:
                data=xml_file_name+" is Missing Series ID"
                missing_fields.append(data)
            if t5!=1:
                data=xml_file_name+" is Missing Season ID"
                missing_fields.append(data)
            if t6!=1:
                data=xml_file_name+" is Missing Episode ID"
                missing_fields.append(data)
            if t7!=1:
                data=xml_file_name+" is Missing Episode Production Number"
                missing_fields.append(data)
            if t8!=1:
                data=xml_file_name+" is Missing Show Type"
                missing_fields.append(data)
            if t9!=1:
                data=xml_file_name+" is Missing Season Number"
                missing_fields.append(data)
            if t10!=1:
                data=xml_file_name+" is Missing Release Date"
                missing_fields.append(data)
            if t11!=1:
                data=xml_file_name+" is Missing Original Release Year" #asset class missing
                missing_fields.append(data)
            if t12!=1:
                data=xml_file_name+" is Missing Genre"
                missing_fields.append(data)
            if t13!=1:
                data=xml_file_name+" is Missing Video File Name"
                missing_fields.append(data)
            if t14!=1:
                data=xml_file_name+" is Missing Captions File Name"
                missing_fields.append(data)
            if t15!=1:
                data=xml_file_name+" is Missing Image File Name"
                missing_fields.append(data)
            if t16!=1:
                data=xml_file_name+" is Missing Sales Start Date"
                missing_fields.append(data)

            email =  str('\n'.join([str(x) for x in missing_fields]))
            server.sendmail("testintegrate2017@gmail.com", "michael.vanderlyn@verizondigitalmedia.com", email)
            server.quit()
            del missing_fields[0]
            return ['Invalid',missing_fields]
