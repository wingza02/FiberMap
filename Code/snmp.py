from easysnmp import Session
from db import *

#For Connection SNMP.----------------------------------------------------------
def connSession(ip,comString):
    snmp = Session(hostname=ip, community=comString, version=2)
    return snmp

#For Device Table.-------------------------------------------------------------
def nameDevice(snmp,oid):
    # name = snmp.get('.1.3.6.1.2.1.1.5.0')
    name = snmp.get(oid[0]['oid'])
    return name.value

# def modelDevice(snmp):
#     model = snmp.get('.1.3.6.1.2.1.1.1.0')
#     return model.value

# def isCoreDevice(snmp):
#     name = snmp.get('.1.3.6.1.2.1.1.5.0')
#     if name.value == '6K_ENG':
#         return 1
#     elif name.value == '6K_AGR':
#         return 1
#     elif name.value == 'VSS_COM.cm.edu':
#         return 1
#     elif name.value == '6K_MED':
#         return 1
#     elif name.value == 'MEAHEA_3750_Main':
#         return 1
#     elif name.value == '4K_Maehea':
#         return 1
#     else:
#         return 0

def upTimeDevice(snmp,oid):
    # uptime = snmp.get('.1.3.6.1.2.1.1.3.0')
    uptime = snmp.get(oid[1]['oid'])
    return uptime.value 

#For Port Table.---------------------------------------------------------------
def ifType(snmp,db,nameAll,oid):
    name = []
    name2 = []
    oidname = []
    oidname2 = []
    oidport = []
    port = []
    data = []
    iftype = []
    # nameAll = checkdevice(db)

    # cdpname = snmp.walk('.1.3.6.1.4.1.9.9.23.1.2.1.1.6')
    cdpname = snmp.walk(oid[2]['oid'])
    for i in cdpname:
        oidname.append(i.oid)
        name.append(i.value)
    for i in range (len(name)):
        for j in range (len(nameAll)):
            if name[i]==nameAll[j]:
                name2.append(name[i])
                # oidname2.append(oidname[i].split('.')[14])
                oidname2.append(oidname[i].split('.')[oid[2]['slot']])

    # iftype = snmp.walk('.1.3.6.1.2.1.2.2.1.2')
    iftype = snmp.walk(oid[3]['oid'])
    for item in iftype:
        oidport.append(item.oid.split('.')[oid[3]['slot']])
        port.append(item.value)
    for j in range (len(oidname2)) :
        for i in range (len(oidport)):
            if oidname2[j] == oidport[i]:
                data.append(port[i])
    return data

def ifOper(snmp,db,nameAll,oid):
    name = []
    name2 = []
    oidname = []
    oidname2 = []
    oidoper = []
    oper = []
    data = []
    # nameAll = checkdevice(db)

    # cdpname = snmp.walk('.1.3.6.1.4.1.9.9.23.1.2.1.1.6')
    cdpname = snmp.walk(oid[2]['oid'])
    for i in cdpname:
        oidname.append(i.oid)
        name.append(i.value)
    for i in range (len(name)):
        for j in range (len(nameAll)):
            if name[i]==nameAll[j]:
                name2.append(name[i])
                # oidname2.append(oidname[i].split('.')[14])
                oidname2.append(oidname[i].split('.')[oid[2]['slot']])

    # ifoper = snmp.walk('.1.3.6.1.2.1.2.2.1.8')
    ifoper = snmp.walk(oid[4]['oid'])
    for item in ifoper:
        # oidoper.append(item.oid.split('.')[10])
        oidoper.append(item.oid.split('.')[oid[4]['slot']])
        oper.append(item.value)
    for j in range (len(oidname2)) :
        for i in range (len(oidoper)):
            if oidname2[j] == oidoper[i]:
                data.append(oper[i])
    return data

#For Connect Table.------------------------------------------------------------
def cdpName(snmp,db,nameAll,oid):
    name = []
    name2 = []
    oidname = []
    oidname2 = []
    oidif = []
    iftype = []
    data = []
    # nameAll = checkdevice(db)
    # cdpname = snmp.walk('.1.3.6.1.4.1.9.9.23.1.2.1.1.6')
    cdpname = snmp.walk(oid[2]['oid'])
    for i in cdpname:
        oidname.append(i.oid)
        name.append(i.value)

    for i in range(len(name)):
        for j in range(len(nameAll)):
            if(nameAll[j]==name[i]):
                name2.append(name[i])
                # oidname2.append(oidname[i].split('.')[14])
                oidname2.append(oidname[i].split('.')[oid[2]['slot']])

    if_type = snmp.walk(oid[4]['oid'])
    for item in if_type:
        oidif.append(item.oid.split('.')[oid[4]['slot']])
        iftype.append(item.value)

    for i in range (len(oidname2)) :
        for j in range (len(oidif)):
            if oidname2[i] == oidif[j]:
                data.append(name2[i])
    return data

def cdpIf(snmp,db,nameAll,oid):
    name = []
    name2 = []
    oidname = []
    oidname2 = []
    oidif = []
    iftype = []
    data = []
    # nameAll = checkdevice(db)
    # cdpname = snmp.walk('.1.3.6.1.4.1.9.9.23.1.2.1.1.6')
    cdpname = snmp.walk(oid[2]['oid'])
    for i in cdpname:
        oidname.append(i.oid)
        name.append(i.value)

    for i in range(len(name)):
        for j in range(len(nameAll)):
            if(nameAll[j]==name[i]):
                name2.append(name[i])
                # oidname2.append(oidname[i].split('.')[14])
                oidname2.append(oidname[i].split('.')[oid[2]['slot']])
    
    # cdpport = snmp.walk('.1.3.6.1.4.1.9.9.23.1.2.1.1.7')
    cdpport = snmp.walk(oid[5]['oid'])
    for item in cdpport:
        # oidif.append(item.oid.split('.')[14])
        oidif.append(item.oid.split('.')[oid[5]['slot']])
        iftype.append(item.value)

    for i in range (len(oidname2)) :
        for j in range (len(oidif)):
            if oidname2[i] == oidif[j]:
                if(len(iftype[j])<5):
                    iftype[j] = iftype[j][:2] + 'gabitethernet' +iftype[j][2:]
                data.append(iftype[j])
    return data

#For Usage Table.-----------------------------------------------------------------------
def inbound(snmp,db,nameAll):
    name = []
    name2 = []
    oidname = []
    oidname2 = []
    oidinbound = []
    in_bound = []
    data = []
    # nameAll = checkdevice(db)
    cdpname = snmp.walk('.1.3.6.1.4.1.9.9.23.1.2.1.1.6')
    for i in cdpname:
        oidname.append(i.oid)
        name.append(i.value)

    for i in range(len(name)):
        for j in range(len(nameAll)):
            if(nameAll[j]==name[i]):
                name2.append(name[i])
                oidname2.append(oidname[i].split('.')[14])
    
    inbound = snmp.walk('.1.3.6.1.2.1.31.1.1.1.6')
    for item in inbound:
        oidinbound.append(item.oid.split('.')[11])
        in_bound.append(item.value)

    for i in range (len(oidname2)) :
        for j in range (len(oidinbound)):
            if oidname2[i] == oidinbound[j]:
                data.append(inbound[j].value)
    return data

def outbound(snmp,db,nameAll):
    name = []
    name2 = []
    oidname = []
    oidname2 = []
    oidoutbound = []
    out_bound = []
    data = []
    # nameAll = checkdevice(db)
    cdpname = snmp.walk('.1.3.6.1.4.1.9.9.23.1.2.1.1.6')
    for i in cdpname:
        oidname.append(i.oid)
        name.append(i.value)

    for i in range(len(name)):
        for j in range(len(nameAll)):
            if(nameAll[j]==name[i]):
                name2.append(name[i])
                oidname2.append(oidname[i].split('.')[14])
    
    outbound = snmp.walk('.1.3.6.1.2.1.31.1.1.1.10')
    for item in outbound:
        oidoutbound.append(item.oid.split('.')[11])
        out_bound.append(item.value)

    for i in range (len(oidname2)) :
        for j in range (len(oidoutbound)):
            if oidname2[i] == oidoutbound[j]:
                data.append(out_bound[j])
    return data

def ifSpeed(snmp,db,nameAll):
    name = []
    name2 = []
    oidname = []
    oidname2 = []
    oidifspedd = []
    ifspeed = []
    data = []
    # nameAll = checkdevice(db)
    cdpname = snmp.walk('.1.3.6.1.4.1.9.9.23.1.2.1.1.6')
    for i in cdpname:
        oidname.append(i.oid)
        name.append(i.value)

    for i in range(len(name)):
        for j in range(len(nameAll)):
            if(nameAll[j]==name[i]):
                name2.append(name[i])
                oidname2.append(oidname[i].split('.')[14])
    
    # if_speed = snmp.walk('.1.3.6.1.2.1.2.2.1.5') # unit = bps
    if_speed = snmp.walk('.1.3.6.1.2.1.31.1.1.1.15')  # unit = Mbps
    for item in if_speed:
        # oidifspedd.append(item.oid.split('.')[10]) # unit = bps
        oidifspedd.append(item.oid.split('.')[11]) # unit = Mbps
        ifspeed.append(item.value)

    for i in range (len(oidname2)) :
        for j in range (len(oidifspedd)):
            if oidname2[i] == oidifspedd[j]:
                data.append(ifspeed[j])
    return data


def cpu_usage(snmp):
    cpu = snmp.get('.1.3.6.1.4.1.9.9.109.1.1.1.1.4.1')
    return cpu.value


# hostip = '6620b8a1-5300-4960-8216-a7fa010d027f.mysql.sequelizer.com'
# user = 'hobwnazvithvqnlb'
# passw = '5VdoKgY86ypbdzuGh5tV4Ajs4FtYYXMbBR8uhabkRd5hT3U3zSRSoNhBKSsdV8hh'
# dbase = 'db6620b8a1530049608216a7fa010d027f'
# db = connectdb(hostip,user,passw,dbase)

# snmp = connSession('192.168.101.253','cmumrtg')
# print upTimeDevice(snmp)


