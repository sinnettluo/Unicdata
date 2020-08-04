#-*- coding: UTF-8 -*-
import pandas
import sys
# sys
reload(sys)
sys.setdefaultencoding('utf8')

#funcs
__all__ = [ 'savecar', 'savecarfinal','saveerror','conclose' ]

def savecar(caritems,website,mysqldb,savesize=1000):
    if len(caritems)==savesize:
        df = pandas.DataFrame(caritems)
        caritems = []
        df.to_sql(name=website, con=mysqldb, flavor='mysql', if_exists='append', index=False)
    return caritems

def savecarfinal(caritems,website,mysqldb,savesize=1000):
    if len(caritems)!=savesize and len(caritems)!=0:
        df = pandas.DataFrame(caritems)
        df.to_sql(name=website, con=mysqldb, flavor='mysql', if_exists='append', index=False)

def saveerror(counts,url,website,mysqldb):
    d = {'counts': counts, 'url': url}
    dferror = pandas.DataFrame(data=d, index=["counts", "url"])
    dferror.to_sql(name=website + '_error', con=mysqldb, flavor='mysql', if_exists='append', index=False)

def conclose(mysqldb,mysqldbc):
    try:
        mysqldb.close()
        mysqldbc.close()
    except:
        print 'Close con error'