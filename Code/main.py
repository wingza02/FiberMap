from easysnmp import Session
import MySQLdb
import time,os,sys,json
from snmp import *
from db import *
from line import *
from mongo import *


hostip = ''
user = ''
passw = ''
dbase = ''

time_sleep = 300 # Unit = Second
i=0
j=0
try:
    db = connectdb(hostip,user,passw,dbase)
    host = getIp(db)
    nameAll = checkdevice(db)
    for item in range (len(host)):
        try:
            chk = 0
            snmp = connSession(host[item]['ip'],"cmumrtg")

#################################################################################
            oid = getOID(db,host[item]['model'])
            name = nameDevice(snmp,oid)
            ip = host[item]['id']
            uptime = int(upTimeDevice(snmp,oid))/100

            if checkdevice1(db,name) == 1:
                updatedevice(db,name,ip,uptime)
                print('updateDevice : '+name)
            else:
                insertdevice(db,name,ip,uptime)
                print('insertdevice : '+ name)

##################################################################################

            device_id = checkid(db,name)
            typeport = ifType(snmp,db,nameAll,oid)
            ifoper = ifOper(snmp,db,nameAll,oid)
            chkcore = checkcore(db,name)

            for i in range (len(typeport)):
                try:
                    chk = 0
                    print(typeport[i])
                    if checkport(db,device_id,typeport[i])==device_id:
                        chk = 1
                    if chk == 1:
                        if(int(line_checkstat(db,name,typeport[i]))!=int(ifoper[i])):
                            dataline = line_senddata(db,int(device_id),typeport[i])
                            notify_line(ifoper[i],dataline)
                            updateport(db,device_id,typeport[i],ifoper[i])
                        if(chkcore==1):
                            updateconnect(db,device_id,typeport[i],ifoper[i])
                        if(chkcore==0 and checkconnect2(db,str(device_id),str(typeport[i]))==1):
                            updateconnect(db,device_id,typeport[i],ifoper[i])                    
                    else:
                        insertport(db,device_id,typeport[i],ifoper[i])
                        if(chkcore==1):
                            neiname = cdpName(snmp,db,nameAll,oid)
                            neiport = cdpIf(snmp,db,nameAll,oid)
                            if(checkconnect(db,str(device_id),str(typeport[i]),str(checkid(db,neiname[i])),str(neiport[i]))!=1):
                                insertconnect(db,device_id,typeport[i],ifoper[i],checkid(db,neiname[i]),neiport[i])                      
                        if(chkcore==0 and checkconnect1(db,str(device_id),str(typeport[i]))==0):
                            neiname = cdpName(snmp,db,nameAll,oid)
                            neiport = cdpIf(snmp,db,nameAll,oid)
                            if(checkcore(db,neiname[i]) == 1):
                                continue
                            else:
                                if(checkconnect(db,str(device_id),str(typeport[i]),str(checkid(db,neiname[i])),str(neiport[i]))!=1):
                                    insertconnect(db,device_id,typeport[i],ifoper[i],checkid(db,neiname[i]),neiport[i])

#####################################################################################
                except Exception as e:
                    print('Interface Fail : ' + str(e))
                    iscore = faildevice_if(db,host[item]['ip'])
                    if (iscore == 1) :
                        faildevice_connect(db,host[item]['ip'])

#####################################################################################

        except Exception as e:
            try:
                print('device Fail : ' + str(e))
                fail_idname = checkidbyip(db,host[item]['ip'])
                failport = findportbyid(db,fail_idname[0])
                for i in range(len(failport)):
                    if(int(line_checkstat(db,fail_idname[1],failport[i]['typeport'])) != 0):
                        dataline = line_senddata(db,int(fail_idname[0]),failport[i]['typeport'])
                        notify_line('0',dataline)
                faildevice_uptime(db,host[item]['ip'])
                iscore = faildevice_if(db,host[item]['ip'])
                faildevice_connect(db,host[item]['ip'])
            except Exception as error:
                print(str(error))
                print('No Device in Database or Cannot Connect to Device')
except Exception as e:
    print('Internet Problem')
    print(str(e))
closedb(db)