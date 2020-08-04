# -*- coding: utf-8 -*-

import os
import time

class Redial(object):
    def __init__(self):
        self.name = "ppp0"
        self.username = "admin"
        self.password = "admin"

    def connect(self):
        cmd_str = "/sbin/ifup %s" % self.name
        response = os.system(cmd_str)
        if(response == 0):
            print("connect successful")
        else:
            print(response)
        time.sleep(2)


    def disconnect(self):
        cmdstr="/sbin/ifdown %s" % self.name
        response = os.system(cmdstr)
        print(response)
        time.sleep(2)


    def reconnect(self):
        self.disconnect()
        self.connect()

if __name__ == "__main__":
    redail = Redial()
    redail.connect()

