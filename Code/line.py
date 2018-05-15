from easysnmp import Session
import MySQLdb
import time
from snmp import *
from db import *
import requests

hostip = '4b6453fd-8951-419f-886f-a8c70109f09c.mysql.sequelizer.com'
user = 'fybpwnvoyhyyqgbl'
passw = 'hBP7UoPdHrbLmvuyaWgbBY5D2XvEDCeqLfd7AGV7q8dKEmwK5G7Xha8qEjf6ZiGe'
dbase = 'db4b6453fd8951419f886fa8c70109f09c'

# hostip = 'dc69c330-09ef-4391-9e84-a8b301659dd0.mysql.sequelizer.com'
# user = 'sbphieacqlqffwde'
# passw = 'jdk4feDo3NKe6cTUWCEqUFjZe3TnhABhLpYaJxrLEwxPG5hKQZyTwYwK3tXmtrfz'
# dbase = 'dbdc69c33009ef43919e84a8b301659dd0'
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