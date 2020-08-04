#-*- coding: UTF-8 -*-

import pymongo
import MySQLdb
#bloomfilter
import pybloom
#md5
import hashlib
import sys
# sys
reload(sys)
sys.setdefaultencoding('utf8')

#funcs
__all__ = ['ParseInit', 'MongoInit','Mysql_Init','Mysql_Counts','Bloom_Init','bloom_check' ,'ParseprocessInit']

#basesetting
def ParseInit(website):
    #params
    params =dict()
    #website
    params['website'] = website

    #mongo
    params['mongocoll']=params['website']
    params['mongoip']="192.168.1.92"
    params['mongoport']=27017
    params['mongodbname']="usedcar"

    #mysql
    params['mysqltable']=params['website']
    params['mysqlip']="192.168.1.92"
    params['mysqluser']="root"
    params['mysqlpasswd']="Datauser@2016"
    params['mysqldbname']="usedcar"
    params['mysqlport']=3306

    #df
    params['bfrate']=0.001
    #counts
    params['keycol']="statusplus"

    #carinfocreate
    params['carinfocreate'] = False
    #counts
    params['counts']=0
    #size
    params['savesize']=1000

    return params

#basesetting
def ParseprocessInit(params):
    # params
    website = params['website']
    carinfocreate=params['carinfocreate']
    counts = params['counts']
    savesize=params['savesize']
    mysqltable=params['mysqltable']

    #mongo
    mongoparams=MongoInit(mongocoll=params['mongocoll'],mongoip=params['mongoip'],mongoport=params['mongoport'],mongodbname=params['mongodbname'])

    connection=mongoparams[0]
    collection=mongoparams[1]
    #mysql
    mysqlparams=Mysql_Init(createsql=params['createsql'],mysqlip=params['mysqlip'],mysqluser=params['mysqluser'],mysqlpasswd=params['mysqlpasswd'],mysqldbname=params['mysqldbname'],mysqlport=params['mysqlport'])
    mysqldb = mysqlparams[0]
    mysqldbc = mysqlparams[1]

    #Bloom
    df = Bloom_Init(mysqltable=params['mysqltable'],collection=collection,mysqldbc=mysqldbc,bfrate=params['bfrate'],keycol=params['keycol'])

    return [website,carinfocreate,counts,savesize,mysqltable,connection,collection,mysqldb,mysqldbc,df]


def MongoInit(mongocoll,mongoip="192.168.1.92",mongoport=27071,mongodbname="usedcar"):
    # mongo
    connection = pymongo.MongoClient(mongoip,mongoport)
    db = connection[mongodbname]
    collection = db[mongocoll]
    param=[connection,collection]
    return param

def Mysql_Init(createsql,mysqlip="192.168.1.92",mysqluser="dataUser94",mysqlpasswd="Datauser@2016",mysqldbname="usedcar",mysqlport=3306):
    #mysql
    mysqldb = MySQLdb.connect(mysqlip, mysqluser, mysqlpasswd, mysqldbname,port=mysqlport)
    mysqldbc = mysqldb.cursor()
    #mysql setting
    mysqldb.set_character_set('utf8')
    mysqldbc.execute('SET NAMES utf8mb4;')
    mysqldbc.execute('SET CHARACTER SET utf8mb4;')
    mysqldbc.execute('SET character_set_connection=utf8mb4;')
    mysqldbc.execute(createsql)
    param = [mysqldb, mysqldbc]
    return param

def Mysql_Counts(mysqltable,mysqlip="192.168.1.92",mysqluser="dataUser94",mysqlpasswd="Datauser@2016",mysqldbname="usedcar",mysqlport=3306):
    #mysql
    mysqldb = MySQLdb.connect(mysqlip, mysqluser, mysqlpasswd, mysqldbname,port=mysqlport)
    mysqldbc = mysqldb.cursor()
    sql ="SELECT COUNT(*) FROM "+mysqltable
    try:
        mysqldbc.execute(sql)
        results =mysqldbc.fetchall()
        for row in results:
            counts = row[0]
    except:
        counts=0
    mysqldb.close()
    return counts

def Bloom_Init(mysqltable,collection,mysqldbc,bfrate=0.001,keycol="statusplus"):
    # pybloom
    num = collection.count() * 1.1
    df = pybloom.BloomFilter(capacity=num, error_rate=bfrate)
    # read
    mysqldbc.execute("select "+ keycol+" from " + mysqltable)
    items = mysqldbc.fetchall()
    for i in items:
        item = hashlib.md5(i[0]).hexdigest()
        df.add(item)
    return df

def bloom_check(status,df):
    try:
        md5i = hashlib.md5(status).hexdigest()
        returndf = df.add(md5i)
    except:
        returndf = False
    return returndf