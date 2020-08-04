#-*- coding: UTF-8 -*-
import re
import sys
import time
import datetime
import MySQLdb
import scrapy

# sys
reload(sys)
sys.setdefaultencoding('utf8')


def parse_routine(caritemlist, item, domtext):
    caritemcontent = dict()
    for caritem in caritemlist:
        # if caritem['colname'] == 'post_time':
        #     print(caritem['mainstring']+":post_time")
        caritemcontent[caritem['colname']] = parse(
            tag=caritem['tag'],
            mainstring=caritem['mainstring'],
            restring=caritem['restring'],
            redeal=caritem['redeal'],
            strip=caritem['strip'],
            formatstring=caritem['format'],
            formula=caritem['formula'],
            extractstring=caritem['extract'],
            lenstring=caritem['lenstring'],
            addstring=caritem['addstring'],
            formatbeforestring=caritem['format_before'],
            hx2car = caritem['hx2car'],
            chewang=caritem['chewang'],
            souhu=caritem['souhu'],
            itemdata=item,
            domcontent=domtext
        )
    return caritemcontent

def ILikeParse(caritemlist,item,domtext):
    length=len(caritemlist)
    versionnumber=length/103
    currentversion=1
    i=(currentversion-1)*103
    j=currentversion*103

    parsed_item=parse_routine(caritemlist[i:j],item,domtext)
    while(currentversion<=versionnumber):
        if keycolscheck(parsed_item):
            return parsed_item
        currentversion = currentversion + 1
        i = (currentversion - 1) * 103
        j = currentversion * 103
        print(str(currentversion) + ":version")
        parsed_item = parse_routine(caritemlist[i:j], item, domtext)
    # return parsed_item

def keycolscheck(caritemcontent):
    print(str(caritemcontent['post_time'])+':post_time')
    keycols = ["shortdesc", "registerdate", "price1"]
    returncode = 1
    for cols in keycols:
        print(str(caritemcontent[cols])+cols)
        if not (caritemcontent[cols]):
            returncode = 0
            break
    return returncode


def parse(tag, mainstring, restring, redeal, strip, formatstring, formula, extractstring, lenstring, addstring,
          formatbeforestring, hx2car, chewang, souhu, itemdata, domcontent):
    # main parsew
    if tag == "time":
        caritemdata = time.strftime(mainstring, time.localtime())
    elif tag == "item":
        caritemdata = itemdata[mainstring]
    elif tag == "value":
        caritemdata = mainstring
    elif tag == "text":
        caritemdata = domcontent.response.body
    elif tag == "xpath":

        xpathcontent = ""
        mainstring = eval("u'%s'" % mainstring)
        try:
            xpathcontent = domcontent.xpath(mainstring)
        except Exception as e:
            print(str(e) + mainstring)
        if xpathcontent:
            if extractstring == "alljoin":
                caritemdata = "".join(xpathcontent.extract())

            else:
                caritemdata = xpathcontent.extract_first()
        else:
            caritemdata = None
    else:
        caritemdata = None
    # re deal
    if restring and caritemdata:

        restring = eval("u'%s'" % restring)
        revalue = re.compile(restring).findall(caritemdata)
        if revalue:
            if not (redeal):
                caritemdata = revalue[0]
            elif redeal == ".join":
                caritemdata = ".".join(revalue)
            elif redeal == "-join":
                caritemdata = "-".join(revalue)
        else:
            caritemdata = None
    # strip
    if strip and caritemdata:
        caritemdata = caritemdata.strip()
    ############formula###########
    ############format###########
    if caritemdata and formatstring and formatbeforestring:
        try:
            formatstring = eval("u'%s'" % formatstring)
            formatbeforestring = eval("u'%s'" % formatbeforestring)
            caritemdata = time.strftime(formatstring, time.strptime(caritemdata, formatbeforestring))
        except:
            caritemdata = caritemdata

    ###########addstring#########
    if caritemdata and addstring:
        addstring = eval("u'%s'" % addstring)
        caritemdata = caritemdata + addstring
    elif not (caritemdata) and addstring:
        addstring = eval("u'%s'" % addstring)
        caritemdata = addstring
    ############len###########
    if caritemdata and len(caritemdata) >= int(lenstring):
        caritemdata = caritemdata[:int(lenstring)]

    if hx2car:
        hx2car = eval("u'%s'" % hx2car)
        hx2car_xpathcontent = ""
        try:
            hx2car_xpathcontent = domcontent.xpath(hx2car).extract_first()
        except Exception as e:
            print(str(e) + hx2car)
        if hx2car_xpathcontent:
            caritemdata = caritemdata + hx2car_xpathcontent
            # print("hx2car" + caritemdata.decode('utf8'))

    if chewang:
        chewang = eval("u'%s'" % chewang)
        chewang_xpathcontent = ""
        try:
            chewang_xpathcontent = domcontent.xpath(chewang).extract_first()
        except Exception as e:
            print(str(e) + chewang)
        if chewang_xpathcontent:
            chewang_xpathcontent = re.findall(u"含(.*?)元", chewang_xpathcontent)[0]
            caritemdata = float(caritemdata) - float(chewang_xpathcontent)/10000

    if souhu:
        souhu = eval("u'%s'" % souhu)
        souhu_xpathcontent = ""
        try:
            souhu_xpathcontent = domcontent.xpath(souhu).extract_first()
        except Exception as e:
            print(str(e) + souhu)
        if souhu_xpathcontent:
            price1 = re.findall(u"￥(.*?)万", souhu_xpathcontent)[0]
            caritemdata = float(caritemdata) + float(price1)

    return caritemdata



# def Parse_conf(website, mysqlip="localhost", mysqluser="dataUser94", mysqlpasswd="root",
#                mysqldbname="usedcar_update", mysqlport=3306):

def Parse_conf(website, mysqlip="192.168.1.94", mysqluser="dataUser94", mysqlpasswd="Datauser@2017",
               mysqldbname="usedcar_update", mysqlport=3306):
    # mysql
    mysqldb = MySQLdb.connect(mysqlip, mysqluser, mysqlpasswd, mysqldbname, port=mysqlport, charset="utf8")
    mysqldbc = mysqldb.cursor()
    sql = "SELECT * FROM parse_conf where website='" + website + "'"
    caritemlist = []
    try:
        mysqldbc.execute(sql)
        results = mysqldbc.fetchall()
        print(results)
        caritemlist = []
        for row in results:
            caritem = dict()
            caritem['ID'] = row[0]
            caritem['itemid'] = row[2]
            caritem['version'] = row[3]
            caritem['colname'] = row[4]
            caritem['tag'] = row[5]
            caritem['status'] = row[6]
            caritem['mainstring'] = row[7]
            caritem['restring'] = row[8]
            caritem['redeal'] = row[9]
            caritem['strip'] = row[10]
            caritem['format'] = row[11]
            caritem['formula'] = row[12]
            caritem['extract'] = row[13]
            caritem['lenstring'] = row[14]
            caritem['addstring'] = row[15]
            caritem['format_before'] = row[16]
            caritem['hx2car'] = row[18]
            caritem['chewang'] = row[19]
            caritem['souhu'] = row[20]
            caritemlist.append(caritem)
    except:
        print "error"
    mysqldb.close()
    return caritemlist