from easysnmp import Session
import MySQLdb
import time,os,sys,json
from snmp import *
from db import *
from line import *
from mongo import *
from config import ip,lat,lng


hostip = '4b6453fd-8951-419f-886f-a8c70109f09c.mysql.sequelizer.com'
user = 'fybpwnvoyhyyqgbl'
passw = 'hBP7UoPdHrbLmvuyaWgbBY5D2XvEDCeqLfd7AGV7q8dKEmwK5G7Xha8qEjf6ZiGe'
dbase = 'db4b6453fd8951419f886fa8c70109f09c'

# hostip = 'dc69c330-09ef-4391-9e84-a8b301659dd0.mysql.sequelizer.com'
# user = 'sbphieacqlqffwde'
# passw = 'jdk4feDo3NKe6cTUWCEqUFjZe3TnhABhLpYaJxrLEwxPG5hKQZyTwYwK3tXmtrfz'
# dbase = 'dbdc69c33009ef43919e84a8b301659dd0'


# cur_path = os.path.abspath(os.path.dirname(sys.argv[0]))
# address_path = os.path.join(cur_path,'config.json')
# addressFile = open(address_path)
# host = json.load(addressFile)
# addressFile.close()

#createdb(db)
time_sleep = 300 # Unit = Second
i=0
j=0
lastid_cpu = autoInc_cpu()
lastid_bandwidth = autoInc_bandwidth()

# while True:
try:
    db = connectdb(hostip,user,passw,dbase)
    host = getIp(db)
    nameAll = checkdevice(db)
    for item in range (len(host)):
        try:
            chk = 0
            snmp = connSession(host[item]['ip'],"cmumrtg")

#################################################################################
            name = nameDevice(snmp)
            model = 'cisco'
            ip = host[item]['id']
            iscore = isCoreDevice(snmp) # Wait Change
            uptime = int(upTimeDevice(snmp))/100

            if checkdevice1(db,name) == 1:
                updatedevice(db,name,ip,uptime)
                print('updateDevice : '+name)
            else:
                insertdevice(db,name,model,ip,uptime)
                print('insertdevice : '+ name)

##################################################################################
            device_id = checkid(db,name)
            typeport = ifType(snmp,db,nameAll)
            ifoper = ifOper(snmp,db,nameAll)
            band_in = inbound(snmp,db,nameAll)
            band_out = outbound(snmp,db,nameAll)
            ifspeed = ifSpeed(snmp,db,nameAll)
            chkcore = checkcore(db,name)
            # print('checkcore: ' + str(chkcore))
            # print('device_id: ' + str(device_id))
            for i in range (len(typeport)):
                # print(typeport[i])
                try:
                    chk = 0
                    # print(device_id)
                    print(typeport[i])
                    if checkport(db,device_id,typeport[i])==device_id:
                        chk = 1
                    if chk == 1:
                        if(int(line_checkstat(db,name,typeport[i]))!=int(ifoper[i])):
                            dataline = line_senddata(db,int(device_id),typeport[i])
                            # print device_id
                            # print typeport[i]
                            # print(dataline)
                            notify_line(ifoper[i],dataline)
                            updateport(db,device_id,typeport[i],ifoper[i])
                            # print('updateport : '+typeport[i])
                        # print line_checkstat(db,name,typeport[i])
                        # print typeport[i]
                        # print band_in[i]
                        # print band_out[i]
                        # print ifspeed[i]
                        if(chkcore==1):
                            updateconnect(db,device_id,typeport[i],ifoper[i])
                            lastid_bandwidth = lastid_bandwidth+1
                            mongo_bandwidth(lastid_bandwidth,device_id,typeport[i],band_in[i],band_out[i],ifspeed[i])
                        
                        if(chkcore==0 and checkconnect2(db,str(device_id),str(typeport[i]))==1):
                            updateconnect(db,device_id,typeport[i],ifoper[i])
                            lastid_bandwidth = lastid_bandwidth+1
                            mongo_bandwidth(lastid_bandwidth,device_id,typeport[i],band_in[i],band_out[i],ifspeed[i])
                    
                    else:
                        insertport(db,device_id,typeport[i],ifoper[i])
                        if(chkcore==1):
                            neiname = cdpName(snmp,db,nameAll)
                            neiport = cdpIf(snmp,db,nameAll)
                            if(checkconnect(db,str(device_id),str(typeport[i]),str(checkid(db,neiname[i])),str(neiport[i]))!=1):
                                insertconnect(db,device_id,typeport[i],ifoper[i],checkid(db,neiname[i]),neiport[i])
                            lastid_bandwidth = lastid_bandwidth+1
                            mongo_bandwidth(lastid_bandwidth,device_id,typeport[i],band_in[i],band_out[i],ifspeed[i])    
                        
                        if(chkcore==0 and checkconnect1(db,str(device_id),str(typeport[i]))==0):
                            neiname = cdpName(snmp,db,nameAll)
                            neiport = cdpIf(snmp,db,nameAll)
                            if(checkcore(db,neiname[i]) == 1):
                                continue
                            else:
                                if(checkconnect(db,str(device_id),str(typeport[i]),str(checkid(db,neiname[i])),str(neiport[i]))!=1):
                                    insertconnect(db,device_id,typeport[i],ifoper[i],checkid(db,neiname[i]),neiport[i])
                                lastid_bandwidth = lastid_bandwidth+1
                                mongo_bandwidth(lastid_bandwidth,device_id,typeport[i],band_in[i],band_out[i],ifspeed[i])  
                        # print 'insertport'
                
                except Exception as e:
                    # notify_crash(str(e))
                    # have not int fail but only have db error
                    print('Interface Fail : ' + str(e))
                    iscore = faildevice_if(db,host[item]['ip'])
                    if (iscore == 1) :
                        faildevice_connect(db,host[item]['ip'])

#####################################################################################

            cpu = cpu_usage(snmp)
            # print cpu
            lastid_cpu = lastid_cpu+1
            mongo_cpu(lastid_cpu,device_id,cpu)
            # closedb(db)
        except Exception as e:
            try:
                # notify_crash(str(e))
                print('device Fail : ' + str(e))
                # name_fail = devicefail(db,host[item]['address']['ip'])
                # if(devicefail3 != 0):
                    # notify_device(0,name_fail)
                    # devivefail2(db,name_fail)

                fail_idname = checkidbyip(db,host[item]['ip'])
                failport = findportbyid(db,fail_idname[0])
                for i in range(len(failport)):
                    if(int(line_checkstat(db,fail_idname[1],failport[i]['typeport'])) != 0):
                        dataline = line_senddata(db,int(fail_idname[0]),failport[i]['typeport'])
                        # print(dataline)
                        notify_line('0',dataline)
                
                faildevice_uptime(db,host[item]['ip'])
                iscore = faildevice_if(db,host[item]['ip'])
                # if (iscore == 1 or (iscore == 0 and checkconnect2(db,str(device_id),str(typeport[i]))==1)) :
                faildevice_connect(db,host[item]['ip'])
            except Exception as error:
                print(str(error))
                print('No Device in Database or Cannot Connect to Device')
        # closedb(db)
except Exception as e:
    print('Internet Problem')
    print(str(e))
j+=1
print str(j) +'Round'
closedb(db)
# time.sleep(time_sleep)