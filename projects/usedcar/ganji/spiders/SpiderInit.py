#-*- coding: UTF-8 -*-
import pymongo
from pybloom import BloomFilter
from hashlib import md5
import os
from scrapy.conf import settings
import re

#original
def spider_original_Init(dbname, website, carnum):
    # Mongo setting
    settings.set('CrawlCar_Num', carnum, priority='cmdline')
    settings.set('MONGODB_DB', dbname, priority='cmdline')
    settings.set('MONGODB_COLLECTION', website, priority='cmdline')

#new
def spider_new_Init(spidername,dbname, website, carnum,urltag='url',keycol='url'):
    #Mongo setting
    # spider_original_Init(dbname, website, carnum)
    # Mongo con
    connection = pymongo.MongoClient(
        settings['MONGODB_SERVER'],
        settings['MONGODB_PORT']
    )
    dbdata = connection[dbname]
    collectiondata = dbdata[website]

    # bloom file
    filename = 'blm/' + dbname + '/' + spidername + ".blm"
    # pybloom
    num = int((int(carnum) + collectiondata.count()) * 1.1)
    df = BloomFilter(capacity=num, error_rate=0.001)
    # read
    isexists = os.path.exists(filename)
    fa = open(filename, "a")
    itemmax =0
    if isexists:
        fr = open(filename, "r")
        lines = fr.readlines()
        for line in lines:
            line = line.strip('\n')
            df.add(line)
        fr.close()
    else:
        for i in collectiondata.find():
            if keycol in i.keys():
                if urltag=='url':
                    item = i[keycol]
                    itemmd5 = md5(item).hexdigest()
                    returndf = df.add(itemmd5)
                    if not (returndf):
                        fa.writelines(itemmd5 + '\n')
                else:
                    item = re.findall('\d+',i["url"])
                    item = int(item [len(item)-1])
                    if item > itemmax:
                        itemmax = item
        if urltag=='num':
            for item in range(1,itemmax+1):
                item =str(item)
                itemmd5 = md5(item).hexdigest()
                returndf = df.add(itemmd5)
                if not (returndf):
                    fa.writelines(itemmd5 + '\n')
    fa.close()
    connection.close()
    return df

#update
def spider_update_Init(dbname, website, carnum):

    # Mongo setting
    # spider_original_Init(dbname, website, carnum)
    # Mongo con
    connection = pymongo.MongoClient(
        settings['MONGODB_SERVER'],
        settings['MONGODB_PORT']
    )
    dbdata = connection[dbname]
    collectiondata = dbdata[website]

    # pybloom
    num = (int(carnum) + collectiondata.count()) * 1.1
    df = BloomFilter(capacity=num, error_rate=0.01)

    # urllist
    urllist = []
    for i in collectiondata.find():
        if "url" in i.keys():
            item = i["url"]
            if "status" in i.keys():
                if not(i['status'].find('sold')==-1):
                    continue
            itemmd5 = md5(item).hexdigest()
            returndf = df.add(itemmd5)
            if not (returndf):
                urllist.append(item)
    connection.close()
    return urllist

def dfcheck(df, item, tag):
    if tag=='new':
        itemmd5 = md5(item).hexdigest()
        returndf = df.add(itemmd5)
        return returndf
    else :
        return False

def dffile(fa, item, tag,urltag='url'):
    if tag=='new' and urltag=='url':
        itemmd5 = md5(item).hexdigest()
        fa.writelines(itemmd5 + '\n')
        return fa
    elif tag=='new' and urltag=='num':
        item = re.findall('\d+', item)
        item = str(item[len(item) - 1])
        itemmd5 = md5(item).hexdigest()
        fa.writelines(itemmd5 + '\n')
        return fa
    else :
        return fa