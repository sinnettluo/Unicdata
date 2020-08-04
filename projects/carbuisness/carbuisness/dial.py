import os
import time
import socket
import urllib
import urllib2
# from subprocess import call

import shlex
import datetime
import subprocess

socket.setdefaulttimeout(180)

apiUrl = 'http://xxx.com/push/ip'
token = 'bd934b846164f97a1f15bca8d64cec51'
vpn = '1'
g_adsl_account = {"name": "adsl",
                  "username": "adsl账号",
                  "password": "adsl密码"}


class Adsl(object):
    def __init__(self):
        self.name = g_adsl_account["name"]
        self.username = g_adsl_account["username"]
        self.password = g_adsl_account["password"]

    def connect(self):
        try:
            cmd_str = "rasdial %s %s %s" % (
                self.name, self.username, self.password)
            self.execute_command(cmd_str, None, 10)
            # stauts = os.system(cmd_str)
            # print os.popen(cmd_str).read()
            # print os.popen('rasdial').read()
            # call(cmd_str)
            localtime = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            print "status: connect; current: %s" % localtime
            time.sleep(5)
        except:
            self.reconnect()

    def disconnect(self):
        self.execute_command("taskkill /F /IM rasdial.exe", None, 10)
        cmd_str = "rasdial %s /disconnect" % self.name
        self.execute_command(cmd_str, None, 10)
        # os.system(cmd_str)
        # call(cmd_str)
        localtime = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        print "status: disconnect; current: %s" % localtime
        time.sleep(5)

    def reconnect(self):
        self.disconnect()
        self.connect()
        self.handleIp()

    def handleIp(self):
        localtime = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        localIPList = socket.gethostbyname_ex(socket.gethostname())
        ip = localIPList[2][-1]
        print "get Ip: %s; current: %s" % (ip, localtime)
        try:
            values = {'ip': ip, 'access_token': token, 'vpn': vpn}
            data = urllib.urlencode(values)
            req = urllib2.Request(apiUrl, data)
            response = urllib2.urlopen(req, timeout=180)
            status = response.read().decode('utf-8', 'ignore')
            self.getStatus(status)
        except:
            self.getStatus(0)

    def getStatus(self, status):
        localtime = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        print "status: %s; current: %s" % (status, localtime)
        if status == '1':
            print 'sleep: 180 second'
            time.sleep(180)
            self.reconnect()
        else:
            print 'status: reconnect'
            self.reconnect()

    def execute_command(self, cmdstring, cwd=None, timeout=None, shell=False):
        if shell:
            cmdstring_list = cmdstring
        else:
            cmdstring_list = shlex.split(cmdstring)
        if timeout:
            end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        sub = subprocess.Popen(cmdstring_list, cwd=cwd,
                               stdin=subprocess.PIPE, shell=shell, bufsize=4096)
        while sub.poll() is None:
            time.sleep(0.1)
            if timeout:
                if end_time <= datetime.datetime.now():
                    raise Exception('Timeout: %s' % cmdstring)

        return str(sub.returncode)


adsl = Adsl()
adsl.reconnect()