from easysnmp import Session
import MySQLdb
import time
from snmp import *
from db import *
import requests

hostip = ''
user = ''
passw = ''
dbase = ''

try:
    db = connectdb(hostip,user,passw,dbase)
except Exception as e:
    print(str(e))

def notify_line(status,data):
    paras = data
    name = getAllName(db)
    for i in range(len(name)):
        if(paras[1]==name[i]['id']):
            nameA = name[i]['name']
        if(int(paras[3])==name[i]['id']):
            nameB = name[i]['name']
    # print name

    # print paras
    # print nameA
    # print nameB
    # print paras[1]
    url = 'https://fibermap.herokuapp.com/line?status='+status+'&A='+nameA+'&port_A='+str(paras[2])+'&B='+nameB+'&port_B='+str(paras[4])
    requests.get(url)

def notify_device(status,name):
    paras = name
    url = 'https://fibermap.herokuapp.com/line_device?status='+status+'&name='+name

def notify_crash(event):
    url = 'https://fibermap.herokuapp.com/line_crash?event='+event
    requests.get(url)