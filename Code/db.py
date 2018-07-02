#!/usr/bin/python
import MySQLdb

def connectdb(host,username,pwd,database):
	db = MySQLdb.connect(host,username,pwd,database)
	return db

def closedb(db):
	db.cursor().close()

##############################################################################################
def insertdevice(db,name,ip,uptime):
	cursor = db.cursor()
	sql = """INSERT INTO `device`(`name`,`ip_addr`, `uptime`) VALUES ('%s','%d','%d')""" %(name,ip,uptime)
	try:
   		cursor.execute(sql)
   		db.commit()
	except:
   		db.rollback()

def insertport(db,device_id,typeport,status_id):
	cursor = db.cursor()
	sql = """INSERT INTO port(device_id,typeport,status_id)
         VALUES ('%s','%s','%s')""" %(device_id,typeport,status_id)
	try:
   		cursor.execute(sql)
   		db.commit()
	except:
   		db.rollback()

def insertconnect(db,device_id,device_port,port_status,connect_device,connect_port):
	cursor = db.cursor()
	sql = """INSERT INTO connection(device_id,port_device,port_status,connect_device,connect_port)
         VALUES ('%d','%s','%d','%s','%s')""" %(device_id,device_port,int(port_status),connect_device,connect_port)
	try:
   		cursor.execute(sql)
   		db.commit()
	except:
   		db.rollback()

def inserttype(db,type):
	cursor = db.cursor()
	sql = """INSERT INTO typeline(type)
         VALUES ('%s')""" %(type)
	try:
   		cursor.execute(sql)
   		db.commit()
	except:
   		db.rollback()

def insertstatus(db,status):
	cursor = db.cursor()
	sql = """INSERT INTO status(status)
         VALUES ('%s')""" %(status)
   	try:
   		cursor.execute(sql)
   		db.commit()
	except:
   		db.rollback()
	
# def insertbandwidth(db,device_id,if_type,inbound,outbound,ifspeed):
# 	cursor = db.cursor()
# 	sql = ("INSERT INTO `bandwidth`(`device_id`, `if_type`, `inbound`, `outbound`, `ifspeed`) VALUES ("+str(device_id)+",'"+if_type+"',"+str(inbound)+","+str(outbound)+","+str(ifspeed)+")")
# 	try:
#    		cursor.execute(sql)
#    		db.commit()
# 	except:
#    		db.rollback()

# def insertcpu(db,device_id,cpu):
# 	cursor = db.cursor()
# 	sql = ("INSERT INTO cpu(device_id,cpu)VALUES ("+str(device_id)+","+str(cpu)+")")
#    	try:
#    		cursor.execute(sql)
#    		db.commit()
# 	except:
#    		db.rollback()

##############################################################################################
def updatedevice(db,name,ip,uptime):
	cursor = db.cursor()
	sql = """UPDATE `device` SET ip_addr = '%d' ,`uptime`='%d' WHERE `name` = '%s'""" %(ip,uptime,name)
	try:
   		cursor.execute(sql)
   		db.commit()
	except:
		db.rollback()

def updateport(db,device_id,typeport,ifoper):
	cursor = db.cursor()
	sql = """UPDATE port SET status_id = '%s' WHERE device_id = '%s' AND typeport = '%s'""" %(ifoper,device_id,typeport)
   	cursor.execute(sql)
   	try:
   		cursor.execute(sql)
   		db.commit()
	except:
   		db.rollback()

def updateconnect(db,device_id,typeport,ifoper):
	cursor = db.cursor()
	sql = """UPDATE `connection` SET `port_status`= '%s' WHERE `device_id` = '%s' AND port_device = '%s'""" %(ifoper,device_id,typeport)
   	cursor.execute(sql)
   	try:
   		cursor.execute(sql)
   		db.commit()
	except:
   		db.rollback()

##############################################################################################
def checkid(db,name):
	cursor = db.cursor()
	sql = """SELECT id FROM `device` WHERE name = '%s'"""%(name)
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		return row[0]
		
def checkdevice(db):
	name = []
	cursor = db.cursor()
	sql = """SELECT name FROM `device` WHERE 1"""
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		name.append(row[0])
	return name

def getAllName(db):
	name = []
	cursor = db.cursor()
	sql = """SELECT id,name FROM `device` WHERE 1"""
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		data = {"id":row[0],"name":row[1]}
		name.append(data)
	return name

def checkdevice1(db,name):
	cursor = db.cursor()
	sql = ("SELECT id FROM device WHERE name = '"+name+"'")
	cursor.execute(sql)
	results = cursor.fetchone()
	# print results
	if(results!=None):
		return 1
	else:
		return 0

def checkport(db,device_id,typeport):
	d_id = []
	cursor = db.cursor()
	sql = """SELECT `device_id` 
			FROM `port` 
			WHERE device_id = '%d' AND typeport = '%s'"""%(device_id,typeport)
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		return row[0]

def checkcore(db,name):
	d_id = []
	cursor = db.cursor()
	sql = """SELECT d2.is_core FROM device AS d1 JOIN ip AS d2 ON d1.ip_addr=d2.id WHERE name = '%s' """%(name)
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		return row[0]

def getIp(db):
	data = []
	cursor = db.cursor()
	sql=("SELECT * FROM ip")
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		temp = {"id": int(row[0]), "ip": row[1], "model":row[6]}
		data.append(temp)
	return data

def getOID(db,model):
	data = []
	cursor = db.cursor()
	sql=("SELECT d1.id, d1.oid, d1.slot FROM model_oid AS d1 INNER JOIN model AS d2 ON d1.model_id = d2.id WHERE d2.model = '"+model+"' ORDER BY d1.descript asc")
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		temp = {"id": int(row[0]), "oid": row[1], "slot":row[2]}
		data.append(temp)
	return data

def checkidbyip(db,ip):
	cursor = db.cursor()
	sql = ("SELECT d1.id,d1.name FROM device AS d1 INNER JOIN ip AS d2 ON (d1.ip_addr = d2.id) WHERE d2.ip = '"+str(ip)+"'")
	cursor.execute(sql)
	results = cursor.fetchone()
	return results

def findportbyid(db,id):
	data = []
	cursor = db.cursor()
	sql = ("SELECT device_id,typeport FROM port WHERE device_id = '"+str(id)+"'")
	cursor.execute(sql)
	results = cursor.fetchall()
	for i in results:
		temp = {'device_id':i[0], 'typeport':i[1]}
		data.append(temp)
	return data

def checkconnect(db,device_id,device_port,nei_id,nei_port):
	cursor = db.cursor()
	sql = ("SELECT * FROM connection WHERE device_id = '"+nei_id+"' AND port_device = '"+nei_port+"' AND connect_device = '"+device_id+"' AND connect_port = '"+device_port+"'")
	cursor.execute(sql)
	results = cursor.fetchone()
	if(results != None):
		return 1
	else:
		return 0

def checkconnect1(db,device_id,device_port):
	cursor = db.cursor()
	sql = ("SELECT * FROM connection WHERE connect_device = '"+device_id+"' AND connect_port = '"+device_port+"'")
	cursor.execute(sql)
	results = cursor.fetchone()
	if(results != None):
		return 1
	else:
		return 0

def checkconnect2(db,device_id,device_port):
	cursor = db.cursor()
	sql = ("SELECT * FROM connection WHERE device_id = '"+device_id+"' AND port_device = '"+device_port+"'")
	cursor.execute(sql)
	results = cursor.fetchone()
	if(results != None):
		return 1
	else:
		return 0

##############################################################################################
def line_checkstat(db,name,typeport):
	cursor = db.cursor()
	sql = ("SELECT port.id,device.id, port.typeport, port.status_id FROM port INNER JOIN device ON port.device_id=device.id WHERE device.name = '"+name+"' AND port.typeport = '"+typeport+"';")
	cursor.execute(sql)
	data = cursor.fetchone()
	return data[3]

def line_senddata(db,_id,typeport):
	cursor = db.cursor()
	sql = """SELECT connection.id,connection.device_id, connection.port_device, connection.connect_device,connection.connect_port FROM connection INNER JOIN device ON connection.device_id=device.id WHERE (connection.device_id = '%d' AND connection.port_device = '%s') OR (connection.connect_device = '%d' AND connection.connect_port = '%s');"""%(_id,typeport,_id,typeport)
	cursor.execute(sql)
	data = cursor.fetchone()
	return data

##############################################################################################
def devicefail(db,ip):
	cursor = db.cursor()
	sql = ("SELECT name FROM device WHERE ip_addr='"+ip+"';")
	cursor.execute(sql)
	data = cursor.fetchone()
	return data[0]

def devicefail2(db,name):
	cursor = db.cursor()
	sql = """UPDATE `device` SET `uptime`=0 WHERE `name` = '%s'""" %(name)
	try:
   		cursor.execute(sql)
   		db.commit()
	except:
		db.rollback()

def devicefail3(db,name):
	cursor = db.cursor()
	sql = ("SELECT uptime FROM device WHERE name='"+name+"';")
	cursor.execute(sql)
	data = cursor.fetchone()
	return data[0]

def faildevice_uptime(db,ip_addr):
	cursor = db.cursor()
	sql = ("SELECT d1.id FROM device AS d1 JOIN ip AS d2 ON d1.ip_addr=d2.id WHERE d2.ip='"+ip_addr+"';")
	cursor.execute(sql)
	data = cursor.fetchone()
	sql = """UPDATE `device` SET `uptime`= 0 WHERE `id` = '%d'""" %(data[0])
	try:
   		cursor.execute(sql)
   		db.commit()
	except:
		db.rollback()

def faildevice_if(db,ip_addr):
	cursor = db.cursor()
	sql = ("SELECT d1.id, d2.is_core FROM device AS d1 JOIN ip AS d2 ON d1.ip_addr=d2.id WHERE d2.ip='"+ip_addr+"';")
	cursor.execute(sql)
	data = cursor.fetchall()
	for i in (data):
		device_id = i[0]
		isCore = i[1]
	sql = """UPDATE `port` SET `status_id`= 0 WHERE `device_id` = '%s'""" %(device_id)
	try:
   		cursor.execute(sql)
   		db.commit()
	except:
		db.rollback()
	return isCore
	
def faildevice_connect(db,ip_addr):
	cursor = db.cursor()
	sql = ("SELECT d1.id FROM device AS d1 JOIN ip AS d2 ON d1.ip_addr=d2.id WHERE d2.ip='"+ip_addr+"';")
	cursor.execute(sql)
	data = cursor.fetchone()
	device_id = data[0]
	# print device_id
	sql = """UPDATE `connection` SET `port_status`= 0 WHERE `device_id` = '%s'""" %(device_id)
	try:
   		cursor.execute(sql)
   		db.commit()
	except:
		db.rollback()


# hostip = 'dc69c330-09ef-4391-9e84-a8b301659dd0.mysql.sequelizer.com'
# user = 'sbphieacqlqffwde'
# passw = 'jdk4feDo3NKe6cTUWCEqUFjZe3TnhABhLpYaJxrLEwxPG5hKQZyTwYwK3tXmtrfz'
# dbase = 'dbdc69c33009ef43919e84a8b301659dd0'
# db = connectdb(hostip,user,passw,dbase)
# print(checkidbyip(db,str('192.168.101.254'))[1])
# print(findportbyid(db,34))
# print(checkconnect1(db,'71','GigabitEthernet1/0/6'))
# closedb(db)
# print(getIp(db))
# print(checkconnect(db,'2','TenGigabitEthernet5/4','5','TenGigabitEthernet1/1/2'))
# # did = checkid(db,'PHAR_2960S.cmu')
# # print checkport(db,did,'GigabitEthernet1/0/25')
# # print checkcore(db,'LIB_2960G')
# # print(checkid(db,'6K_ENG'))
# print line_senddata(db,'6K_ENG','GigabitEthernet1/6')
