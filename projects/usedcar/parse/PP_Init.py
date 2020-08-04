#-*- coding: UTF-8 -*-
#parellel
import pp
#取整
import math
#格式转换
import json
import sys
# sys
reload(sys)
sys.setdefaultencoding('utf8')
#load funcs
from Parse_Init import *

#funcs
__all__ = [ 'ppInit']

def ppInit(params,parts):
    #mysql
    mysqlcounts=Mysql_Counts(mysqltable=params['mysqltable'],mysqlip=params['mysqlip'],mysqluser=params['mysqluser'],mysqlpasswd=params['mysqlpasswd'],mysqldbname=params['mysqldbname'],mysqlport=params['mysqlport'])
    # mongo
    mongoparams=MongoInit(mongocoll=params['mongocoll'],mongoip=params['mongoip'],mongoport=params['mongoport'],mongodbname=params['mongodbname'])
    connection=mongoparams[0]
    collection=mongoparams[1]

    # Calculates pp_params
    pp_params=dict()
    pp_params['start'] = mysqlcounts
    pp_params['end'] = collection.count()
    connection.close()
    # Since jobs are not equal in the execution time, division of the problem
    # into a 100 of small subproblems leads to a better load balancing
    pp_params['step'] = (pp_params['end'] - pp_params['start']) / parts+1
    return pp_params