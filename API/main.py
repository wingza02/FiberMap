import json , falcon , requests, datetime, dateutil.relativedelta, time, pymongo
import MySQLdb
from dateutil import parser
from pymongo import MongoClient
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError
from linebot.models import StickerSendMessage
from falcon_cors import CORS

dbase = '4b6453fd-8951-419f-886f-a8c70109f09c.mysql.sequelizer.com'
user = 'fybpwnvoyhyyqgbl'
passw = 'hBP7UoPdHrbLmvuyaWgbBY5D2XvEDCeqLfd7AGV7q8dKEmwK5G7Xha8qEjf6ZiGe'
dbname = 'db4b6453fd8951419f886fa8c70109f09c'

# dbase = 'dc69c330-09ef-4391-9e84-a8b301659dd0.mysql.sequelizer.com'
# user = 'sbphieacqlqffwde'
# passw = 'jdk4feDo3NKe6cTUWCEqUFjZe3TnhABhLpYaJxrLEwxPG5hKQZyTwYwK3tXmtrfz'
# dbname = 'dbdc69c33009ef43919e84a8b301659dd0'

line_bot_api = LineBotApi("yAYsucZj4IEsk4zhe+GtxYanhLGymJHtOybtl0SvbvX8fY0Jdky4An+1QeU/YGDMUtTD7RelZVmyeGHibqz17+a4wlsWhE4b+LDz8wNEAzccVoKZUg2rvdZ527bULGquoE+Wx2RWrQJbuC+Zj92D3AdB04t89/1O/w1cDnyilFU=")

cors = CORS(allow_origins_list=['http://localhost:8080/'],)
api = falcon.API(middleware=[cors.middleware])
public_cors = CORS(allow_all_origins=True,allow_all_headers=True,allow_all_methods=True,allow_credentials_all_origins=True)

class home:
    def on_get(self,req,resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        with open('index.html', 'r') as f:
            resp.body = f.read()

class ObjRequestClass:
    cors = public_cors
    def on_get(self,req,resp):
        resp.status = falcon.HTTP_200
        # data = json.loads(req.stream.read())
        data = {"name":"Ballza2017"}
        output = {
            'msg' : 'hello {0}'.format(data['name'])
        }
        resp.body = json.dumps(output)

    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200
        data = json.loads(req.stream.read())
        eq = int(data['x'])+int(data['y'])
        output = {
            'msg' : 'x : {0} + y : {1} = {2}'.format(data['x'],data['y'],eq)
        }
        resp.body = json.dumps(output)

class getip:
    cors = public_cors
    def on_get(self,req,resp):
        resp.status = falcon.HTTP_200
        db = MySQLdb.connect(dbase,user,passw,dbname)
        cursor = db.cursor()
        resp.status = falcon.HTTP_200
        data = []
        cursor.execute("SELECT * FROM ip WHERE 1;")
        req_data = cursor.fetchall()
        for i in req_data:
            temp = {"id":i[0], "ip":i[1], "lat":i[2], "lng":i[3], "is_core":i[4]}
            data.append(temp)
        resp.body = json.dumps(data)

class getswitch:
    cors = public_cors
    def on_post(self, req , resp):
        resp.status = falcon.HTTP_200
        data = json.loads(req.stream.read())
        cursor.execute("SELECT name FROM device WHERE id = "+data['id'])
        dataeiei = cursor.fetchone()
        eiei = {"version":dataeiei , "x":data['x'] , "y":data['y']}
        resp.body = json.dumps(eiei)
        
    def on_get(self, req, resp):
        try:
            db = MySQLdb.connect(dbase,user,passw,dbname)
            cursor = db.cursor()
            resp.status = falcon.HTTP_200
            data = []
            cursor.execute("SELECT d1.id, d1.name, d1.model, d2.lat, d2.lng, d2.ip ip_addr, d2.is_core, d1.uptime, d1.timestamp FROM device AS d1 INNER JOIN ip AS d2 ON d1.ip_addr=d2.id;")
            req_data = cursor.fetchall()
            for x in req_data:
                if(x[7]!=0):
                    time = str(datetime.timedelta(seconds=x[7]))
                    temp = {"id":str(x[0]), "name":x[1],"model":x[2],"position":{"lat":float(x[3]),"lng":float(x[4])}, "ip":x[5],"uptime":time,"status":"Up", "is_core":x[6]}
                else:
                    time = str(datetime.timedelta(seconds=x[7]))
                    temp = {"id":str(x[0]), "name":x[1],"model":x[2],"position":{"lat":float(x[3]),"lng":float(x[4])}, "ip":x[5],"uptime":time,"status":"Down", "is_core":x[6]}
                data.append(temp)
            resp.body = json.dumps(data)
            cursor.close()
        except:
            resp.body = json.dumps({"status": 0, "detail":"error"})

class getinterface:
    cors = public_cors
    def on_get(self, req, resp):
        db = MySQLdb.connect(dbase,user,passw,dbname)
        cursor = db.cursor()
        resp.status = falcon.HTTP_200
        data = []
        cursor.execute("SELECT d1.id, d2.name, d1.typeport, d1.status_id FROM port AS d1 INNER JOIN device AS d2 ON d1.device_id = d2.id")
        req_data = cursor.fetchall()
        for x in req_data:
            temp = {"id":x[0], "name":x[1], "type":x[2], "status":x[3]}
            data.append(temp)
        resp.body = json.dumps(data)
        cursor.close()

class connect:
    cors = public_cors
    def on_get(self, req, resp):
        db = MySQLdb.connect(dbase,user,passw,dbname)
        cursor = db.cursor()
        resp.status = falcon.HTTP_200
        data = []
        data2 = []
        sql2 = ("SELECT d1.id, d1.name, d2.lat, d2.lng FROM device AS d1 INNER JOIN ip AS d2 ON d1.ip_addr=d2.id;")
        cursor.execute(sql2)
        req_data = cursor.fetchall()
        for item in req_data:
            temp2 = {"id":item[0], "name":item[1], "lat":float(item[2]), "lng":float(item[3])}
            data2.append(temp2)
        sql = ("SELECT d1.id, d1.device_id, d1.port_device, d1.port_status, d1.connect_device, d1.connect_port, d2.status_id FROM connection AS d1 INNER JOIN port AS d2 ON (d1.connect_device = d2.device_id AND d1.connect_port = d2.typeport) ORDER BY id asc;")
        cursor.execute(sql)
        req_data = cursor.fetchall()
        for item in req_data:
            for i in range(len(data2)):
                if(data2[i]['id']==item[1]):
                    nameA = data2[i]['name']
                    lat_a = data2[i]['lat']
                    lng_a = data2[i]['lng']
                if(data2[i]['id']==int(item[4])):
                    nameB = data2[i]['name']
                    lat_b = data2[i]['lat']
                    lng_b = data2[i]['lng'] 
            if(int(item[3])==1 and int(item[6])==1):
                statusLine = 'Up'
                colorLine = 'GREEN'
            else:
                statusLine = 'Down'
                colorLine = 'RED'
            temp = {"id":item[0], "A":nameA, "port_A":item[2],"status_A":item[3], "B":nameB, "port_B":item[5],"status_B":item[6], "path":[{"lat":float(lat_a), "lng":float(lng_a)}, {"lat":float(lat_b), "lng":float(lng_b) }], "linestatus": statusLine, "linecolor":colorLine}
            data.append(temp)
        resp.body = json.dumps(data)
        cursor.close()

class getInfoline:
    cors = public_cors
    def on_get(self, req, resp):
        db = MySQLdb.connect(dbase,user,passw,dbname)
        cursor = db.cursor()
        resp.status = falcon.HTTP_200
        DataInput = req.params
        cursor.execute("SELECT d1.id, d1.connection_id, d1.distance, d2.type, d1.core_number, d1.patch_panel, d1.connector, d1.timestamp, d1.gmap_distance FROM infoline as d1 INNER JOIN typeline as d2 ON d2.id = d1.type_id WHERE connection_id = '"+DataInput['line_id']+"'")
        req_data = cursor.fetchone()
        try:
            data = {"id":req_data[0], "line_id":req_data[1], "distance":req_data[2], "type":req_data[3], "core_number":req_data[4], "patch":req_data[5], "connector":req_data[6], "timestamp":str(req_data[7]), "gmap_distance":req_data[8]}
        except:
            data = []
        resp.body = json.dumps(data)
        cursor.close()

class getUser:
    cors = public_cors
    def on_get(self, req, resp):
        db = MySQLdb.connect(dbase,user,passw,dbname)
        cursor = db.cursor()
        resp.status = falcon.HTTP_200
        data = []
        DataInput = req.params
        cursor.execute("SELECT * FROM user WHERE 1")
        req_data = cursor.fetchall()
        for i in req_data:
            temp = {"id":i[0], "username":i[1], "firstname":i[3], "lastname":i[4], "tel":i[5], "email":i[6], "isAdmin":i[7], "regDate":str(i[8])}
            data.append(temp)
        resp.body = json.dumps(data)
        cursor.close()

class line:
    cors = public_cors
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        DataInput = req.params
        if DataInput['status']=='0':
            line_bot_api.push_message("Uc1ab017d8ca2412f2019538081e9ad65", TextSendMessage(text=DataInput['A']+" to "+DataInput['B']+ " Status: Down" ))
        elif DataInput['status']=='1':
            line_bot_api.push_message("Uc1ab017d8ca2412f2019538081e9ad65", TextSendMessage(text=DataInput['A']+" to "+DataInput['B']+" Status: Up"))
        else:
            line_bot_api.push_message("Uc1ab017d8ca2412f2019538081e9ad65", TextSendMessage(text="Unknown Status"))

        resp.body=json.dumps({"Status":"Sucess"})

class line_crash():
    cors = public_cors
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        DataInput = req.params
        line_bot_api.push_message("Uc1ab017d8ca2412f2019538081e9ad65", TextSendMessage(text=DataInput['event']))
        resp.body=json.dumps({"Status":"Sucess"})

class showByStatus:
    cors = public_cors
    def on_get(self, req, resp):
        db = MySQLdb.connect(dbase,user,passw,dbname)
        cursor = db.cursor()
        resp.status = falcon.HTTP_200
        DataInput = req.params
        data = []
        data2 = []
        data3 = []
        data4 = []
        sql2 = ("SELECT d1.id, d1.name, d2.lat, d2.lng, d1.model, d2.ip ip_addr, d1.uptime, d1.timestamp FROM device AS d1 INNER JOIN ip AS d2 ON d1.ip_addr=d2.id;")
        cursor.execute(sql2)
        req_data = cursor.fetchall()
        for item in req_data:
            if(item[6]!=0):
                status = "Up" 
            else: 
                status = "Down"
            time = str(datetime.timedelta(seconds=item[6]))
            temp2 = {"id":item[0], "name":item[1],"position":{"lat":float(item[2]), "lng":float(item[3])},"model":item[4],"ip":item[5],"uptime":time,"status":status}
            data2.append(temp2)
        if(int(DataInput['status']))==1:
            sql = ("SELECT d1.id, d1.device_id, d1.port_device,d1.port_status, d1.connect_device, d1.connect_port, d2.status_id FROM .connection AS d1 INNER JOIN .port AS d2 ON (d1.connect_device = d2.device_id AND d1.connect_port = d2.typeport) WHERE (d1.port_status = 1 and d2.status_id = 1) ORDER BY id asc;")
        else:
            sql = ("SELECT d1.id, d1.device_id, d1.port_device,d1.port_status, d1.connect_device, d1.connect_port, d2.status_id FROM .connection AS d1 INNER JOIN .port AS d2 ON (d1.connect_device = d2.device_id AND d1.connect_port = d2.typeport) WHERE d1.port_status = "+DataInput['status']+" or d2.status_id = "+DataInput['status']+" ORDER BY id asc;")
        cursor.execute(sql)
        req_data = cursor.fetchall()
        for item in req_data:
            for i in range(len(data2)):
                if(data2[i]['id']==item[1]):
                    nameA = data2[i]['name']
                    lat_a = data2[i]['position']['lat']
                    lng_a = data2[i]['position']['lng']
                if(data2[i]['id']==int(item[4])):
                    nameB = data2[i]['name']
                    lat_b = data2[i]['position']['lat']
                    lng_b = data2[i]['position']['lng'] 
                if((data2[i]['id']==item[1] or data2[i]['id']==int(item[4])) and data2[i] not in data4):
                    data4.append(data2[i])
            if(int(item[3])==1 and int(item[6])==1):
                statusLine = 'Up'
                colorLine = 'GREEN'
            else:
                statusLine = 'Down'
                colorLine = 'RED'
            temp = {"id":item[0], "A":nameA, "port_A":item[2],"status_A":item[3], "B":nameB, "port_B":item[5],"status_B":item[6], "path":[{"lat":float(lat_a), "lng":float(lng_a)}, {"lat":float(lat_b), "lng":float(lng_b) }], "linestatus": statusLine, "linecolor":colorLine}
            data.append(temp)
        data3 = [{"switch":data4,"connect":data}]
        resp.body = json.dumps(data3)
        cursor.close()

class connectById:
    cors = public_cors
    def on_get(self, req, resp):
        db = MySQLdb.connect(dbase,user,passw,dbname)
        cursor = db.cursor()
        resp.status = falcon.HTTP_200
        DataInput = req.params
        data = []
        data2 = []
        sql2 = ("SELECT d1.id, d1.name, d2.lat, d2.lng, d1.model, d2.ip ip_addr, d1.uptime, d1.timestamp FROM device AS d1 INNER JOIN ip AS d2 ON d1.ip_addr=d2.id")
        cursor.execute(sql2)
        req_data = cursor.fetchall()
        for item in req_data:
            temp2 = {"id":item[0], "name":item[1], "lat":float(item[2]), "lng":float(item[3]),"model":item[4],"ip_addr":item[5],"uptime":item[6]}
            data2.append(temp2)
        sql = ("SELECT d1.id, d1.device_id, d1.port_device, d1.port_status, d1.connect_device, d1.connect_port, d2.status_id FROM connection AS d1 INNER JOIN port AS d2 ON (d1.connect_device = d2.device_id AND d1.connect_port = d2.typeport) WHERE d1.id = '"+DataInput['id']+"' ORDER BY id asc;")
        cursor.execute(sql)
        req_data = cursor.fetchall()
        for item in req_data:
            for i in range(len(data2)):
                if(data2[i]['id']==item[1]):
                    nameA = data2[i]['name']
                    lat_a = data2[i]['lat']
                    lng_a = data2[i]['lng']
                    uptime_a = str(datetime.timedelta(seconds=data2[i]['uptime']))
                if(data2[i]['id']==int(item[4])):
                    nameB = data2[i]['name']
                    lat_b = data2[i]['lat']
                    lng_b = data2[i]['lng']
                    uptime_b = str(datetime.timedelta(seconds=data2[i]['uptime']))
            if(int(item[3])==1 and int(item[6])==1):
                statusLine = 'Up'
                colorLine = 'GREEN'
            else:
                statusLine = 'Down'
                colorLine = 'RED'
            temp = {"switch":[{"id":item[1], "name":nameA,"position":{"lat":float(lat_a),"lng":float(lng_a)}, "uptime":uptime_a},{"id":int(item[4]), "name":nameB,"position":{"lat":float(lat_b),"lng":float(lng_b)}, "uptime":uptime_b}] , "connect":[{"id":item[0], "A":nameA, "port_A":item[2],"status_A":item[3], "B":nameB, "port_B":item[5],"status_B":item[6], "path":[{"lat":float(lat_a), "lng":float(lng_a)}, {"lat":float(lat_b), "lng":float(lng_b) }], "linestatus": statusLine, "linecolor":colorLine}]}
            data.append(temp)
        resp.body = json.dumps(data)
        cursor.close()

class showLayer:
    cors = public_cors
    def on_get(self, req, resp):
        db = MySQLdb.connect(dbase,user,passw,dbname)
        cursor = db.cursor()
        resp.status = falcon.HTTP_200
        data = []
        data2 = []
        data3 = []
        sql2 = ("SELECT d1.id, d1.name, d2.lat, d2.lng, d1.model, d2.ip ip_addr, d1.uptime, d1.timestamp FROM device AS d1 INNER JOIN ip AS d2 ON d1.ip_addr=d2.id WHERE is_core = 1")
        cursor.execute(sql2)
        req_data = cursor.fetchall()
        for item in req_data:
            if(item[6]!=0):
                status = "Up" 
            else: 
                status = "Down"
            time = str(datetime.timedelta(seconds=item[6]))
            temp2 = {"id":item[0], "name":item[1],"position":{"lat":float(item[2]), "lng":float(item[3])},"model":item[4],"ip":item[5],"uptime":time,"status":status}
            data2.append(temp2)
# Wait for Fix ###############################################################################################################################       
        sql = ("SELECT d1.id, d1.device_id, d1.port_device,d1.port_status, d1.connect_device, d1.connect_port, d2.status_id FROM .connection AS d1 INNER JOIN .port AS d2 ON (d1.connect_device = d2.device_id AND d1.connect_port = d2.typeport) WHERE (d1.connect_device=1 or d1.connect_device =2 or d1.connect_device =4 or d1.connect_device=5 or d1.connect_device =33 or d1.connect_device =34) ORDER BY id asc;")
        cursor.execute(sql)
        req_data = cursor.fetchall()
        for item in req_data:
            for i in range(len(data2)):
                if(data2[i]['id']==item[1]):
                    nameA = data2[i]['name']
                    lat_a = data2[i]['position']['lat']
                    lng_a = data2[i]['position']['lng']
                if(data2[i]['id']==int(item[4])):
                    nameB = data2[i]['name']
                    lat_b = data2[i]['position']['lat']
                    lng_b = data2[i]['position']['lng'] 
            if(int(item[3])==1 and int(item[6])==1):
                statusLine = 'Up'
                colorLine = 'GREEN'
            else:
                statusLine = 'Down'
                colorLine = 'RED'
            temp = {"id":item[0], "A":nameA, "port_A":item[2],"status_A":item[3], "B":nameB, "port_B":item[5],"status_B":item[6], "path":[{"lat":float(lat_a), "lng":float(lng_a)}, {"lat":float(lat_b), "lng":float(lng_b) }], "linestatus": statusLine, "linecolor":colorLine}
            data.append(temp)
        data3 = [{"switch":data2,"connect":data}]
        resp.body = json.dumps(data3)
        cursor.close()

class showZone:
    cors = public_cors
    def on_get(self, req, resp):
        db = MySQLdb.connect(dbase,user,passw,dbname)
        cursor = db.cursor()
        resp.status = falcon.HTTP_200
        DataInput = req.params
        data = []
        data2 = []
        data3 = []
        data4 = []
        sql2 = ("SELECT d1.id, d1.name, d2.lat, d2.lng, d1.model, d2.ip ip_addr, d1.uptime, d1.timestamp FROM device AS d1 INNER JOIN ip AS d2 ON d1.ip_addr=d2.id WHERE 1")
        cursor.execute(sql2)
        req_data = cursor.fetchall()
        for item in req_data:
            if(item[6]!=0):
                status = "Up" 
            else: 
                status = "Down"
            time = str(datetime.timedelta(seconds=item[6]))
            temp2 = {"id":item[0], "name":item[1],"position":{"lat":float(item[2]), "lng":float(item[3])},"model":item[4],"ip":item[5],"uptime":time,"status":status}
            data2.append(temp2)
        sql = ("SELECT d1.id, d1.device_id, d1.port_device,d1.port_status, d1.connect_device, d1.connect_port, d2.status_id FROM .connection AS d1 INNER JOIN .port AS d2 ON (d1.connect_device = d2.device_id AND d1.connect_port = d2.typeport) WHERE d1.device_id = "+DataInput['zone']+" ORDER BY id asc;")
        cursor.execute(sql)
        req_data = cursor.fetchall()
        for item in req_data:
            for i in range(len(data2)):
                if(data2[i]['id']==item[1]):
                    nameA = data2[i]['name']
                    lat_a = data2[i]['position']['lat']
                    lng_a = data2[i]['position']['lng']
                    # data4.append(data2[i])
                if(data2[i]['id']==int(item[4])):
                    nameB = data2[i]['name']
                    lat_b = data2[i]['position']['lat']
                    lng_b = data2[i]['position']['lng'] 
                    # data4.append(data2[i])
                if((data2[i]['id']==item[1] or data2[i]['id']==int(item[4])) and data2[i] not in data4):
                    data4.append(data2[i])
            if(int(item[3])==1 and int(item[6])==1):
                statusLine = 'Up'
                colorLine = 'GREEN'
            else:
                statusLine = 'Down'
                colorLine = 'RED'
            # print(data2[i])
            temp = {"id":item[0], "A":nameA, "port_A":item[2],"status_A":item[3], "B":nameB, "port_B":item[5],"status_B":item[6], "path":[{"lat":float(lat_a), "lng":float(lng_a)}, {"lat":float(lat_b), "lng":float(lng_b) }], "linestatus": statusLine, "linecolor":colorLine}
            data.append(temp)
        data3 = [{"switch":data4,"connect":data}]
        resp.body = json.dumps(data3)
        cursor.close()

class saveHistory:
    cors = public_cors
    def on_get(self,req,resp):
        db = MySQLdb.connect(dbase,user,passw,dbname)
        cursor = db.cursor()
        resp.status = falcon.HTTP_200
        DataInput = req.params
        place = 'From: '+DataInput['A']+ ' To: ' +DataInput['B']
        sql = """INSERT INTO history (line_id, comment, distance, status_broken, broken_time, approved_by, status) VALUE ('%d','%s','%f','%d','%s',%d,'%d')"""%(int(DataInput['id']),place,float(DataInput['distance']),1,str(datetime.datetime.now()+datetime.timedelta(hours=7)),int(DataInput['userid']),1)
        try:
            # Execute the SQL command
            cursor.execute(sql)
            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
        cursor.close()

class loadHistory:
    cors = public_cors
    def on_get(self,req,resp):
        db = MySQLdb.connect(dbase,user,passw,dbname)
        cursor = db.cursor()
        data = []
        resp.status = falcon.HTTP_200
        DataInput = req.params
        sql = ("SELECT d1.id, d1.line_id, d1.comment, d1.distance, d1.status_broken, d1.broken_time, d2.firstname AS approved_by, d1.timestamp, d1.status FROM history AS d1 JOIN user AS d2 ON d1.approved_by = d2.id WHERE line_id = '"+DataInput['id']+"' AND status = 1 ORDER BY id DESC;")
        cursor.execute(sql)
        req_data = cursor.fetchall()
        for i in req_data:
            timestamp = i[7] + datetime.timedelta(hours=7)
            temp = {"id":i[0], "line_id":i[1], "comment":i[2], "distance":i[3], "status_broken":i[4], "broken_time":str(i[5]), "approved_by":str(i[6]), "timestamp":str(timestamp), "status":i[8]}
            data.append(temp)
        resp.body = json.dumps({'data':data})
        cursor.close()

class filterHistory:
    cors = public_cors
    def on_get(self,req,resp):
        db = MySQLdb.connect(dbase,user,passw,dbname)
        cursor = db.cursor()
        data = []
        data2 = {}
        time = str(datetime.datetime.now() + datetime.timedelta(hours=7))
        resp.status = falcon.HTTP_200
        DataInput = req.params
        fromDate = datetime.datetime.now() + datetime.timedelta(hours=7) + dateutil.relativedelta.relativedelta(months= int(DataInput['date']))
        sql = ("SELECT d1.id, d1.line_id, d1.comment, d1.distance, d1.status_broken, d1.broken_time, d2.firstname AS approved_by, d1.timestamp, d1.status FROM history AS d1 JOIN user AS d2 ON d1.approved_by = d2.id WHERE line_id = '"+DataInput['id']+"' AND DATE(broken_time) BETWEEN DATE_ADD('"+time+"', INTERVAL '"+DataInput['date']+"' MONTH) AND '"+time+"' AND status=1 ORDER BY id DESC;")
        cursor.execute(sql)
        req_data = cursor.fetchall()
        for i in req_data:
            timestamp = i[7] + datetime.timedelta(hours=7)
            temp = {"id":i[0], "line_id":i[1], "comment":i[2], "distance":i[3], "status_broken":i[4], "broken_time":str(i[5]), "approved_by":str(i[6]), "timestamp":str(timestamp), "status":i[8]}
            data.append(temp)
        time = "{:%Y-%m-%d}".format(datetime.datetime.now() + datetime.timedelta(hours=7))
        fromDate = "{:%Y-%m-%d}".format(fromDate)
        data2 = {'data' : data, 'date' : {'fromDate':fromDate, 'toDate':time}}
        resp.body = json.dumps(data2)
        cursor.close()

class filterHistory2:
    cors = public_cors
    def on_get(self,req,resp):
        db = MySQLdb.connect(dbase,user,passw,dbname)
        cursor = db.cursor()
        data = []
        resp.status = falcon.HTTP_200
        DataInput = req.params
        sql = ("SELECT d1.id, d1.line_id, d1.comment, d1.distance, d1.status_broken, d1.broken_time, d2.firstname AS approved_by, d1.timestamp, d1.status FROM history AS d1 JOIN user AS d2 ON d1.approved_by = d2.id WHERE line_id = '"+DataInput['id']+"' AND DATE(broken_time) BETWEEN DATE_ADD('"+DataInput['fromDate']+"', INTERVAL 0 MONTH) AND DATE_ADD('"+DataInput['toDate']+"', INTERVAL 0 MONTH) AND status=1 ORDER BY id DESC;")
        cursor.execute(sql)
        req_data = cursor.fetchall()
        for i in req_data:
            timestamp = i[7] + datetime.timedelta(hours=7)
            temp = {"id":i[0], "line_id":i[1], "comment":i[2], "distance":i[3], "status_broken":i[4], "broken_time":str(i[5]), "approved_by":str(i[6]), "timestamp":str(timestamp), "status":i[8]}
            data.append(temp)
        resp.body = json.dumps(data)
        cursor.close()

class updateHistory:
    cors = public_cors
    def on_get(self,req,resp):
        db = MySQLdb.connect(dbase,user,passw,dbname)
        cursor = db.cursor()
        resp.status = falcon.HTTP_200
        DataInput = req.params
        place = 'From: '+str(DataInput['A'])+ ' To: ' +str(DataInput['B'])
        sql = """UPDATE history SET status='%d' WHERE id='%d';"""%(0,int(DataInput['id']))
        sql2 = """INSERT INTO history (line_id, comment, distance, status_broken, broken_time, approved_by, status) VALUE ('%d','%s','%f','%d','%s',%d,'%d')"""%(int(DataInput['line_id']),place,float(DataInput['distance']),int(DataInput['status_broken']),str(DataInput['broken_time']),int(DataInput['userid']),1)
        try:
            cursor.execute(sql)
            db.commit()
            time.sleep(0.2)
            cursor.execute(sql2)
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
        cursor.close()

class getHistory:
    cors = public_cors
    def on_get(self,req,resp):
        db = MySQLdb.connect(dbase,user,passw,dbname)
        cursor = db.cursor()
        data = []
        resp.status = falcon.HTTP_200
        DataInput = req.params
        sql = ("SELECT d1.id, d1.line_id, d1.comment, d1.distance, d1.status_broken, d1.broken_time, d2.firstname AS approved_by, d1.timestamp, d1.status FROM history AS d1 JOIN user AS d2 ON d1.approved_by = d2.id WHERE (status_broken = 1 OR status_broken = 2 OR status_broken = 3) AND status = 1 ORDER BY id DESC;")
        cursor.execute(sql)
        req_data = cursor.fetchall()
        for i in req_data:
            timestamp = i[7] + datetime.timedelta(hours=7)
            temp = {"id":i[0], "line_id":i[1], "comment":i[2], "distance":i[3], "status_broken":i[4], "broken_time":str(i[5]), "approved_by":str(i[6]), "timestamp":str(timestamp), "status":i[8]}
            data.append(temp)
        resp.body = json.dumps({'data':data})
        cursor.close()

class getBrokenDistance:
    cors = public_cors
    def on_get(self,req,resp):
        db = MySQLdb.connect(dbase,user,passw,dbname)
        cursor = db.cursor()
        resp.status = falcon.HTTP_200
        data = []
        sql = """SELECT * FROM history WHERE (status_broken = 1 OR status_broken = 2 OR status_broken = 3) AND status=1;"""
        cursor.execute(sql)
        req_data = cursor.fetchall()
        for i in req_data:
            timestamp = i[7] + datetime.timedelta(hours=7)
            temp = {"id":i[0], "line_id":i[1], "comment":i[2], "distance":i[3], "status_broken":i[4], "broken_time":str(i[5]), "timestamp":str(timestamp), "status":i[8]}
            data.append(temp)
        resp.body = json.dumps(data)
        cursor.close()

class getRealpath:
    cors = public_cors
    def on_get(self, req, resp):
        db = MySQLdb.connect(dbase,user,passw,dbname)
        cursor = db.cursor()
        resp.status = falcon.HTTP_200
        temp_colorline = 'Green'
        data = []
        data2 = []
        data3 = []
        sql2 = ("SELECT d1.id, d1.name, d2.lat, d2.lng FROM device AS d1 INNER JOIN ip AS d2 ON d1.ip_addr=d2.id WHERE 1")
        cursor.execute(sql2)
        req_data = cursor.fetchall()
        for item in req_data:
            temp2 = {"id":item[0], "name":item[1], "lat":float(item[2]), "lng":float(item[3])}
            data2.append(temp2)
        sql3 = ("SELECT * FROM polyline WHERE 1")
        cursor.execute(sql3)
        req_data = cursor.fetchall()
        for item in req_data:
            temp3 = {"id":item[0], "lineid":item[1], "seq":item[2], "lat":float(item[3]), "lng":float(item[4]), "colorline":item[5]}
            data3.append(temp3)
        sql = ("SELECT d1.id, d1.device_id, d1.port_device, d1.port_status, d1.connect_device, d1.connect_port, d2.status_id FROM connection AS d1 INNER JOIN port AS d2 ON (d1.connect_device = d2.device_id AND d1.connect_port = d2.typeport);")
        cursor.execute(sql)
        req_data = cursor.fetchall()
        for item in req_data:
            temp_path = ""
            path = []
            for i in range(len(data2)):
                if(data2[i]['id']==item[1]):
                    nameA = data2[i]['name']
                    lat_a = data2[i]['lat']
                    lng_a = data2[i]['lng']
                if(data2[i]['id']==int(item[4])):
                    nameB = data2[i]['name']
                    lat_b = data2[i]['lat']
                    lng_b = data2[i]['lng']
            for i in range(len(data3)):
                if(int(data3[i]['lineid'])==int(item[0])):
                    temp_colorline = data3[i]['colorline']
                    print("Lineid: "+str(data3[i]['lineid']))
                    print("idinConnect: "+str(item[0]))
                    temp_path = {"seq": data3[i]['seq'], "lat": float(data3[i]['lat']), "lng": float(data3[i]['lng'])}
                    path.append(temp_path)
            if(int(item[3])==1 and int(item[6])==1):
                statusLine = 'Up'
                colorLine = temp_colorline
            else:
                statusLine = 'Down'
                colorLine = 'RED'
            temp = {"id":item[0], "A":nameA, "port_A":item[2],"status_A":item[3], "B":nameB, "port_B":item[5],"status_B":item[6], "path": path, "linestatus": statusLine, "linecolor":colorLine}
            data.append(temp)
        resp.body = json.dumps(data)
        cursor.close()

class realpathById:
    cors = public_cors
    def on_get(self, req, resp):
        db = MySQLdb.connect(dbase,user,passw,dbname)
        cursor = db.cursor()
        resp.status = falcon.HTTP_200
        DataInput = req.params
        data = []
        data2 = []
        data3 = []
        sql2 = ("SELECT d1.id, d1.name, d2.lat, d2.lng, d1.model, d2.ip ip_addr, d1.uptime FROM device AS d1 INNER JOIN ip AS d2 ON d1.ip_addr=d2.id WHERE 1")
        cursor.execute(sql2)
        req_data = cursor.fetchall()
        for item in req_data:
            temp2 = {"id":item[0], "name":item[1], "lat":float(item[2]), "lng":float(item[3]), "model":item[4], "ip_addr":item[5], "uptime":item[6]}
            data2.append(temp2)
        sql3 = ("SELECT * FROM polyline WHERE line_id = '"+DataInput['lineid']+"';")
        cursor.execute(sql3)
        req_data = cursor.fetchall()
        for item in req_data:
            temp3 = {"id":item[0], "lineid":item[1], "seq":item[2], "lat":float(item[3]), "lng":float(item[4])}
            data3.append(temp3)
        sql = ("SELECT d1.id, d1.device_id, d1.port_device, d1.port_status, d1.connect_device, d1.connect_port, d2.status_id FROM connection AS d1 INNER JOIN port AS d2 ON (d1.connect_device = d2.device_id AND d1.connect_port = d2.typeport) WHERE d1.id = '"+DataInput['lineid']+"';")
        cursor.execute(sql)
        req_data = cursor.fetchall()
        for item in req_data:
            temp_path = ""
            path = []
            for i in range(len(data2)):
                if(data2[i]['id']==item[1]):
                    nameA = data2[i]['name']
                    lat_a = data2[i]['lat']
                    lng_a = data2[i]['lng']
                    uptime_a = str(datetime.timedelta(seconds=data2[i]['uptime']))
                if(data2[i]['id']==int(item[4])):
                    nameB = data2[i]['name']
                    lat_b = data2[i]['lat']
                    lng_b = data2[i]['lng']
                    uptime_b = str(datetime.timedelta(seconds=data2[i]['uptime']))
            for i in range(len(data3)):
                if(int(data3[i]['lineid'])==int(item[0])):
                    print("Lineid: "+str(data3[i]['lineid']))
                    print("idinConnect: "+str(item[0]))
                    temp_path = {"seq": data3[i]['seq'], "lat": float(data3[i]['lat']), "lng": float(data3[i]['lng'])}
                    path.append(temp_path)
            if(int(item[3])==1 and int(item[6])==1):
                statusLine = 'Up'
                colorLine = '#7FFF00'
            else:
                statusLine = 'Down'
                colorLine = 'RED'
            temp = {"switch":[{"id":item[1], "name":nameA,"position":{"lat":float(lat_a),"lng":float(lng_a)}, "uptime":uptime_a},{"id":int(item[4]), "name":nameB,"position":{"lat":float(lat_b),"lng":float(lng_b)}, "uptime":uptime_b}] , "connect":[{"id":item[0], "A":nameA, "port_A":item[2],"status_A":item[3], "B":nameB, "port_B":item[5],"status_B":item[6], "path": path, "linestatus": statusLine, "linecolor":colorLine}]}
            data.append(temp)
        resp.body = json.dumps(data)
        cursor.close()

class showLayerRP:
    cors = public_cors
    def on_get(self, req, resp):
        db = MySQLdb.connect(dbase,user,passw,dbname)
        cursor = db.cursor()
        resp.status = falcon.HTTP_200
        temp_colorline = 'Green'
        data = []
        data2 = []
        data3 = []
        sql2 = ("SELECT d1.id, d1.name, d2.lat, d2.lng, d1.model, d2.ip ip_addr, d1.uptime FROM device AS d1 INNER JOIN ip AS d2 ON d1.ip_addr=d2.id WHERE is_core = 1")
        cursor.execute(sql2)
        req_data = cursor.fetchall()
        for item in req_data:
            if(item[6]!=0):
                status = "Up" 
            else: 
                status = "Down"
            time = str(datetime.timedelta(seconds=item[6]))
            temp2 = {"id":item[0], "name":item[1],"position":{"lat":float(item[2]), "lng":float(item[3])},"model":item[4],"ip":item[5],"uptime":time,"status":status}
            data2.append(temp2)
        sql3 = ("SELECT * FROM polyline WHERE 1")
        cursor.execute(sql3)
        req_data = cursor.fetchall()
        for item in req_data:
            temp3 = {"id":item[0], "lineid":item[1], "seq":item[2], "lat":float(item[3]), "lng":float(item[4]),"colorline":item[5]}
            data3.append(temp3)
# Wait for Fix ###############################################################################################################################       
        sql = ("SELECT d1.id, d1.device_id, d1.port_device,d1.port_status, d1.connect_device, d1.connect_port, d2.status_id FROM .connection AS d1 INNER JOIN .port AS d2 ON (d1.connect_device = d2.device_id AND d1.connect_port = d2.typeport) WHERE (d1.connect_device=1 or d1.connect_device =2 or d1.connect_device =4 or d1.connect_device=5 or d1.connect_device =33 or d1.connect_device =34) ORDER BY id asc;")
        cursor.execute(sql)
        req_data = cursor.fetchall()
        for item in req_data:
            temp_path = ""
            path = []
            for i in range(len(data2)):
                if(data2[i]['id']==item[1]):
                    nameA = data2[i]['name']
                    lat_a = data2[i]['position']['lat']
                    lng_a = data2[i]['position']['lng']
                if(data2[i]['id']==int(item[4])):
                    nameB = data2[i]['name']
                    lat_b = data2[i]['position']['lat']
                    lng_b = data2[i]['position']['lng'] 
            for i in range(len(data3)):
                if(int(data3[i]['lineid'])==int(item[0])):
                    temp_colorline = data3[i]['colorline']
                    print("Lineid: "+str(data3[i]['lineid']))
                    print("idinConnect: "+str(item[0]))
                    temp_path = {"seq": data3[i]['seq'], "lat": float(data3[i]['lat']), "lng": float(data3[i]['lng'])}
                    path.append(temp_path)
            if(int(item[3])==1 and int(item[6])==1):
                statusLine = 'Up'
                colorLine = temp_colorline
            else:
                statusLine = 'Down'
                colorLine = 'RED'
            temp = {"id":item[0], "A":nameA, "port_A":item[2],"status_A":item[3], "B":nameB, "port_B":item[5],"status_B":item[6], "path":path, "linestatus": statusLine, "linecolor":colorLine}
            data.append(temp)
        data3 = [{"switch":data2,"connect":data}]
        resp.body = json.dumps(data3)
        cursor.close()

class showZoneRP:
    cors = public_cors
    def on_get(self, req, resp):
        db = MySQLdb.connect(dbase,user,passw,dbname)
        cursor = db.cursor()
        resp.status = falcon.HTTP_200
        DataInput = req.params
        temp_colorline = 'Green'
        data = []
        data2 = []
        data3 = []
        data4 = []
        sql2 = ("SELECT d1.id, d1.name, d2.lat, d2.lng, d1.model, d2.ip ip_addr, d1.uptime FROM device AS d1 INNER JOIN ip AS d2 ON d1.ip_addr=d2.id WHERE 1")
        cursor.execute(sql2)
        req_data = cursor.fetchall()
        for item in req_data:
            if(item[6]!=0):
                status = "Up" 
            else: 
                status = "Down"
            time = str(datetime.timedelta(seconds=item[6]))
            temp2 = {"id":item[0], "name":item[1],"position":{"lat":float(item[2]), "lng":float(item[3])},"model":item[4],"ip":item[5],"uptime":time,"status":status}
            data2.append(temp2)
        sql3 = ("SELECT * FROM polyline WHERE 1")
        cursor.execute(sql3)
        req_data = cursor.fetchall()
        for item in req_data:
            temp3 = {"id":item[0], "lineid":item[1], "seq":item[2], "lat":float(item[3]), "lng":float(item[4]), "colorline":item[5]}
            data3.append(temp3)
        sql = ("SELECT d1.id, d1.device_id, d1.port_device,d1.port_status, d1.connect_device, d1.connect_port, d2.status_id FROM .connection AS d1 INNER JOIN .port AS d2 ON (d1.connect_device = d2.device_id AND d1.connect_port = d2.typeport) WHERE d1.device_id = "+DataInput['zone']+" ORDER BY id asc;")
        cursor.execute(sql)
        req_data = cursor.fetchall()
        for item in req_data:
            temp_path = ""
            path = []
            for i in range(len(data2)):
                if(data2[i]['id']==item[1]):
                    nameA = data2[i]['name']
                    lat_a = data2[i]['position']['lat']
                    lng_a = data2[i]['position']['lng']
                    # data4.append(data2[i])
                if(data2[i]['id']==int(item[4])):
                    nameB = data2[i]['name']
                    lat_b = data2[i]['position']['lat']
                    lng_b = data2[i]['position']['lng'] 
                    # data4.append(data2[i])
                if((data2[i]['id']==item[1] or data2[i]['id']==int(item[4])) and data2[i] not in data4):
                    data4.append(data2[i])
            for i in range(len(data3)):
                if(int(data3[i]['lineid'])==int(item[0])):
                    temp_colorline = data3[i]['colorline']
                    print("Lineid: "+str(data3[i]['lineid']))
                    print("idinConnect: "+str(item[0]))
                    temp_path = {"seq": data3[i]['seq'], "lat": float(data3[i]['lat']), "lng": float(data3[i]['lng'])}
                    path.append(temp_path)
            if(int(item[3])==1 and int(item[6])==1):
                statusLine = 'Up'
                colorLine = temp_colorline
            else:
                statusLine = 'Down'
                colorLine = 'RED'
            # print(data2[i])
            temp = {"id":item[0], "A":nameA, "port_A":item[2],"status_A":item[3], "B":nameB, "port_B":item[5],"status_B":item[6], "path":path, "linestatus": statusLine, "linecolor":colorLine}
            data.append(temp)
        data3 = [{"switch":data4,"connect":data}]
        resp.body = json.dumps(data3)
        cursor.close()

class showByStatusRP:
    cors = public_cors
    def on_get(self, req, resp):
        db = MySQLdb.connect(dbase,user,passw,dbname)
        cursor = db.cursor()
        resp.status = falcon.HTTP_200
        DataInput = req.params
        temp_colorline = 'Green'
        data = []
        data2 = []
        data3 = []
        data4 = []
        sql2 = ("SELECT d1.id, d1.name, d2.lat, d2.lng, d1.model, d2.ip ip_addr, d1.uptime FROM device AS d1 INNER JOIN ip AS d2 ON d1.ip_addr=d2.id WHERE 1")
        cursor.execute(sql2)
        req_data = cursor.fetchall()
        for item in req_data:
            if(item[6]!=0):
                status = "Up" 
            else: 
                status = "Down"
            time = str(datetime.timedelta(seconds=item[6]))
            temp2 = {"id":item[0], "name":item[1],"position":{"lat":float(item[2]), "lng":float(item[3])},"model":item[4],"ip":item[5],"uptime":time,"status":status}
            data2.append(temp2)
        sql3 = ("SELECT * FROM polyline WHERE 1")
        cursor.execute(sql3)
        req_data = cursor.fetchall()
        for item in req_data:
            temp3 = {"id":item[0], "lineid":item[1], "seq":item[2], "lat":float(item[3]), "lng":float(item[4]), "colorline":item[5]}
            data3.append(temp3)
        if(int(DataInput['status']))==1:
            sql = ("SELECT d1.id, d1.device_id, d1.port_device,d1.port_status, d1.connect_device, d1.connect_port, d2.status_id FROM .connection AS d1 INNER JOIN .port AS d2 ON (d1.connect_device = d2.device_id AND d1.connect_port = d2.typeport) WHERE (d1.port_status = 1 and d2.status_id = 1) ORDER BY id asc;")
        else:
            sql = ("SELECT d1.id, d1.device_id, d1.port_device,d1.port_status, d1.connect_device, d1.connect_port, d2.status_id FROM .connection AS d1 INNER JOIN .port AS d2 ON (d1.connect_device = d2.device_id AND d1.connect_port = d2.typeport) WHERE d1.port_status = "+DataInput['status']+" or d2.status_id = "+DataInput['status']+" ORDER BY id asc;")
        cursor.execute(sql)
        req_data = cursor.fetchall()
        for item in req_data:
            temp_path = ""
            path = []
            for i in range(len(data2)):
                if(data2[i]['id']==item[1]):
                    nameA = data2[i]['name']
                    lat_a = data2[i]['position']['lat']
                    lng_a = data2[i]['position']['lng']
                if(data2[i]['id']==int(item[4])):
                    nameB = data2[i]['name']
                    lat_b = data2[i]['position']['lat']
                    lng_b = data2[i]['position']['lng'] 
                if((data2[i]['id']==item[1] or data2[i]['id']==int(item[4])) and data2[i] not in data4):
                    data4.append(data2[i])
            for i in range(len(data3)):
                if(int(data3[i]['lineid'])==int(item[0])):
                    temp_colorline = data3[i]['colorline']
                    print("Lineid: "+str(data3[i]['lineid']))
                    print("idinConnect: "+str(item[0]))
                    temp_path = {"seq": data3[i]['seq'], "lat": float(data3[i]['lat']), "lng": float(data3[i]['lng'])}
                    path.append(temp_path)
            if(int(item[3])==1 and int(item[6])==1):
                statusLine = 'Up'
                colorLine = temp_colorline
            else:
                statusLine = 'Down'
                colorLine = 'RED'
            temp = {"id":item[0], "A":nameA, "port_A":item[2],"status_A":item[3], "B":nameB, "port_B":item[5],"status_B":item[6], "path":path, "linestatus": statusLine, "linecolor":colorLine}
            data.append(temp)
        data3 = [{"switch":data4,"connect":data}]
        resp.body = json.dumps(data3)
        cursor.close()

class getCPU:
    cors = public_cors
    def on_get(self, req, resp):
        # db = MySQLdb.connect(dbase,user,passw,dbname)
        # cursor = db.cursor()
        client = MongoClient('mongodb://l3l3allza:123456@ds229549.mlab.com:29549/appharbor_j9h62tbg')
        db = client.appharbor_j9h62tbg
        col = db.cpu
        resp.status = falcon.HTTP_200
        DataInput = req.params
        # days_cpu = []
        # days_time = []
        # months_cpu = []
        # months_time = []
        # years_cpu = []
        # years_time = []
        data = []
        # cursor = col.find({"device_id":int(DataInput['device_id'])})
        # # for x in cursor:
        # #     time = parser.parse(x['timestamp'])
        # #     for i in range(24):
        # #         if (time <= datetime.datetime.now()+datetime.timedelta(hours=7-24)+datetime.timedelta(hours=i) and time >= datetime.datetime.now()+datetime.timedelta(hours=7-24)+datetime.timedelta(hours=i-1)):
        # #             # days_cpu[i] = days_cpu[i] + int(x['cpu'])
        # #             # count[i] = count[i] + 1
        # #             temp = {'round':i,'cpu':x['cpu'], 'time':str(x['timestamp'])}
        # #             data.append(temp)
        # #     # for i in range(len(data)):
        # #     #     if(i == )
        # #     # for i in range(24):
        # #     #     temp_time = "{:%H:%M}".format(datetime.datetime.now()+datetime.timedelta(hours=-24)+datetime.timedelta(hours=i+1))
        # #     #     avg_cpu[i] = avg_day[i]/count[i]
        # #     #     temp = {"avg_cpu":avg_day[i],'time' : temp_time}
        # #     #     data.append(temp)
        # # resp.body = json.dumps(data)
        req_data = col.find({"device_id":int(DataInput['device_id'])})
        for i in req_data:
            temp = {"id":i['_id'], "device_id":i['device_id'], "cpu":i['cpu'], "timestamp":i['timestamp']}
            data.append(temp)
        resp.body = json.dumps(data)

            
# class getCPU:
#     cors = public_cors
#     def on_get(self, req, resp):
#         if (1):
#             # db = MySQLdb.connect(dbase,user,passw,dbname)
#             # cursor = db.cursor()
#             client = MongoClient('mongodb://l3l3allza:123456@ds229549.mlab.com:29549/appharbor_j9h62tbg')
#             db = client.appharbor_j9h62tbg
#             col = db.cpu
#             resp.status = falcon.HTTP_200
#             DataInput = req.params
#             days_cpu = []
#             days_time = []
#             months_cpu = []
#             months_time = []
#             years_cpu = []
#             years_time = []
#             data = []
#             cursor = col.find({"device_id":int(DataInput['device_id'])})
#             # cursor.execute("SELECT * FROM cpu WHERE device_id = '"+DataInput['device_id']+"';")
#             # req_data = cursor.fetchall()
#             for i in range(24):
#                 count = 0
#                 avg_cpu = 0
#                 print(datetime.datetime.now()+datetime.timedelta(hours=7-24)+datetime.timedelta(hours=i))
#                 for x in cursor:
#             #     for x in req_data:
#                     time = parser.parse(x['timestamp'])
#                     if (time <= datetime.datetime.now()+datetime.timedelta(hours=-24)+datetime.timedelta(hours=i) and time >= datetime.datetime.now()+datetime.timedelta(hours=-24)+datetime.timedelta(hours=i-1)):
#                         count = count + 1
#                         avg_cpu = avg_cpu + int(x['cpu'])
#                 if(avg_cpu==0):
#                     avg_cpu=0
#                 else:
#                     avg_cpu=avg_cpu/count
#                 # temp = {"time":"{:%H:%M}".format(datetime.datetime.now()+datetime.timedelta(hours=7)+datetime.timedelta(hours=-i)) , "avg_cpu":avg_cpu}
#                 temp_cpu = avg_cpu
#                 temp_time = "{:%H:%M}".format(datetime.datetime.now()+datetime.timedelta(hours=-24)+datetime.timedelta(hours=i+1))
#                 days_cpu.append(temp_cpu)
#                 days_time.append(temp_time)
#             # for i in range(30):
#             #     count = 0
#             #     avg_cpu = 0
#             #     for x in req_data:
#             #         time = x[3]+datetime.timedelta(hours=7)
#             #         if (time <= datetime.datetime.now()+datetime.timedelta(hours=7)+datetime.timedelta(days=-30+i) and time >= datetime.datetime.now()+datetime.timedelta(hours=7)+datetime.timedelta(days=-30+i-1)):
#             #             count = count + 1
#             #             avg_cpu = avg_cpu + x[2]
#             #     if(avg_cpu==0):
#             #         avg_cpu=0
#             #     else:
#             #         avg_cpu=avg_cpu/count
#             #     # temp = {"time":"{:%H:%M}".format(datetime.datetime.now()+datetime.timedelta(hours=7)+datetime.timedelta(hours=-i)) , "avg_cpu":avg_cpu}
#             #     temp_cpu = avg_cpu
#             #     temp_time = "{:%d %b}".format(datetime.datetime.now()+datetime.timedelta(hours=7)+datetime.timedelta(days=-30+i+1))
#             #     months_cpu.append(temp_cpu)
#             #     months_time.append(temp_time)
#             # for i in range(12):
#             #     count = 0
#             #     avg_cpu = 0
#             #     for x in req_data:
#             #         time = x[3]+datetime.timedelta(hours=7)
#             #         if (time <= datetime.datetime.now()+datetime.timedelta(hours=7)+ dateutil.relativedelta.relativedelta(months=-12+i) and time >= datetime.datetime.now()+datetime.timedelta(hours=7)+ dateutil.relativedelta.relativedelta(months=-12+i-1)):
#             #             count = count + 1
#             #             avg_cpu = avg_cpu + x[2]
#             #     if(avg_cpu==0):
#             #         avg_cpu=0
#             #     else:
#             #         avg_cpu=avg_cpu/count
#             #     # temp = {"time":"{:%H:%M}".format(datetime.datetime.now()+datetime.timedelta(hours=7)+datetime.timedelta(hours=-i)) , "avg_cpu":avg_cpu}
#             #     temp_cpu = avg_cpu
#             #     temp_time = "{:%b %y}".format(datetime.datetime.now()+datetime.timedelta(hours=7)+ dateutil.relativedelta.relativedelta(months=-12+i+1))
#             #     years_cpu.append(temp_cpu)
#             #     years_time.append(temp_time)
#             # data = {'day' : {'cpu':days_cpu,'time':days_time}, 'month' : {'cpu':months_cpu,'time':months_time}, 'year' : {'cpu':years_cpu,'time':years_time}}
#             resp.body = json.dumps(days_cpu)
#             # cursor.close()
#         # except:
#         #     resp.body = json.dumps({"status": 0, "detail":"error"})

class getAllCPU:
    cors = public_cors
    def on_get(self, req, resp):
        client = MongoClient('mongodb://l3l3allza:123456@ds229549.mlab.com:29549/appharbor_j9h62tbg')
        db = client.appharbor_j9h62tbg
        data = []
        resp.status = falcon.HTTP_200
        col = db.cpu
        req_data = col.find()
        for i in req_data:
            temp = {"id":i['_id'], "device_id":i['device_id'], "cpu":i['cpu'], "timestamp":i['timestamp']}
            data.append(temp)
        resp.body = json.dumps(data)

class getAllBW:
    cors = public_cors
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        data = []
        DataInput = req.params
        db = MySQLdb.connect(dbase,user,passw,dbname)
        cursor = db.cursor()
        sql = ("SELECT id FROM device WHERE name like '"+DataInput['name']+"'")
        cursor.execute(sql)
        req_date1 = cursor.fetchone()
        id_device = {"id":req_date1[0]}

        client = MongoClient('mongodb://l3l3allza:123456@ds229549.mlab.com:29549/appharbor_j9h62tbg')
        db = client.appharbor_j9h62tbg
        col = db.bandwidth
        req_data = col.find({'device_id':int(id_device['id']), 'if_type':str(DataInput['type_port'])})
        for i in req_data:
            temp = {"id":i['_id'], "device_id":i['device_id'], "if_type":i['if_type'], "inbound":i['inbound'],"outbound":i['outbound'], "ifspeed":i['ifspeed'], "timestamp":i['timestamp']}
            data.append(temp)
        resp.body = json.dumps(data)

api.add_route('/',home())
# api.add_route('/test',test())#
api.add_route('/test1',ObjRequestClass())
api.add_route('/getswitch',getswitch())
api.add_route('/connect',connect())
api.add_route('/interface',getinterface())
api.add_route('/getip',getip())
api.add_route('/getinfoline',getInfoline())
api.add_route('/getuser',getUser())
api.add_route('/line',line())
api.add_route('/line_crash',line_crash())
api.add_route('/showbystatus',showByStatus())
api.add_route('/connectbyid',connectById())
api.add_route('/showlayer',showLayer())
api.add_route('/showzone',showZone())
api.add_route('/savehistory',saveHistory())
api.add_route('/loadhistory',loadHistory())
api.add_route('/filterhistory',filterHistory())
api.add_route('/filterhistory2',filterHistory2())
api.add_route('/updatehistory',updateHistory())
api.add_route('/gethistory',getHistory())
api.add_route('/getbroken',getBrokenDistance())
api.add_route('/getrealpath',getRealpath())
api.add_route('/realpathbyid',realpathById())
api.add_route('/showlayerRP',showLayerRP())
api.add_route('/showzoneRP',showZoneRP())
api.add_route('/showbystatusRP',showByStatusRP())
api.add_route('/getcpu',getCPU())

api.add_route('/getallcpu',getAllCPU())
api.add_route('/getallbw',getAllBW())



class authUser:
    cors = public_cors
    def on_post(self, req, resp):
        db = MySQLdb.connect(dbase,user,passw,dbname)
        cursor = db.cursor()
        data = []
        resp.status = falcon.HTTP_200
        DataInput = json.loads(req.stream.read())
        sql = ("SELECT * FROM user WHERE username = '"+DataInput['user']+"' && password = '"+DataInput['pass']+"'")
        cursor.execute(sql)
        req_data = cursor.fetchone()
        if(req_data != None):
            if (req_data[7]==0):
                isAdmin = 'false'
            if (req_data[7]==1):
                isAdmin = 'true'
            temp = {"id":req_data[0], "username":req_data[1], "firstname":req_data[3], "lastname":req_data[4], "tel":req_data[5], "email":req_data[6], "isAdmin":isAdmin, "regDate":str(req_data[8])}
            data.append(temp)
        else:
            data  = []
        resp.body = json.dumps(data)
        cursor.close()

class addSwitch:
    cors = public_cors
    def on_get(self, req, resp):
        db = MySQLdb.connect(dbase,user,passw,dbname)
        cursor = db.cursor()
        data = []
        resp.status = falcon.HTTP_200
        DataInput = req.params
        sql = ("INSERT INTO ip (ip,lat,lng,is_core) VALUE ('"+str(DataInput['ip'])+"','"+str(DataInput['lat'])+"','"+str(DataInput['lng'])+"','"+str(DataInput['is_core'])+"')")
        try:
            cursor.execute(sql)
            db.commit()
            resp.body = json.dumps({"status": "success"})
        except:
            db.rollback()
        cursor.close()

class editSwitch:
    cors = public_cors
    def on_get(self, req, resp):
        db = MySQLdb.connect(dbase,user,passw,dbname)
        cursor = db.cursor()
        data = []
        resp.status = falcon.HTTP_200
        DataInput = req.params
        sql = ("UPDATE ip SET ip = '"+DataInput['ip']+"', lat = '"+DataInput['lat']+"', lng = '"+DataInput['lng']+"', is_core = '"+DataInput['is_core']+"' WHERE ip = '"+DataInput['id_ip']+"' ;")
        try:
            cursor.execute(sql)
            db.commit()
            resp.body = json.dumps({"status": "success"})
        except:
            db.rollback()
        cursor.close()

# class deleteSwitch:
#     cors = public_cors
#     def on_get(self, req, resp):
#         db = MySQLdb.connect(dbase,user,passw,dbname)
#         cursor = db.cursor()
#         data = []
#         resp.status = falcon.HTTP_200
#         DataInput = req.params
#         sql = ("DELETE INTO ip (ip,lat,lng,is_core) VALUE ('"+str(DataInput['ip'])+"','"+str(DataInput['lat'])+"','"+str(DataInput['lng'])+"','"+str(DataInput['is_core'])+"')")
#         try:
#             cursor.execute(sql)
#             db.commit()
#         except:
#             db.rollback()
#         cursor.close()

class deleteIp:
    cors = public_cors
    def on_get(self, req, resp):
        db = MySQLdb.connect(dbase,user,passw,dbname)
        cursor = db.cursor()
        data = []
        resp.status = falcon.HTTP_200
        DataInput = req.params
        sql = ("DELETE FROM ip WHERE ip = '"+ DataInput['ip'] +"'")
        try:
            cursor.execute(sql)
            db.commit()
            resp.body = json.dumps({"status": "success"})
        except:
            db.rollback()
        cursor.close()

class addPath:
    cors = public_cors
    def on_post(self, req, resp):
        db = MySQLdb.connect(dbase,user,passw,dbname)
        cursor = db.cursor()
        data = []
        resp.status = falcon.HTTP_200
        DataInput = json.loads(req.stream.read())
        for i in range(len(DataInput['path'])):
            sql = """INSERT INTO polyline (line_id, seq_no, lat, lng, colorline) VALUE ('%d','%d','%s','%s','%s')"""%(int(DataInput['line_id']),int(i+1),str(DataInput['path'][i]['lat']),str(DataInput['path'][i]['lng']),str(DataInput['colorline']))
            cursor.execute(sql)
            db.commit()
            time.sleep(0.2)
        resp.body = json.dumps({"status": "success"})
        cursor.close()

class addInfoLine:
    cors = public_cors
    def on_post(self, req, resp):
        db = MySQLdb.connect(dbase,user,passw,dbname)
        cursor = db.cursor()
        data = []
        resp.status = falcon.HTTP_200
        DataInput = json.loads(req.stream.read())
        sql = """INSERT INTO infoline (connection_id, distance, gmap_distance, type_id, core_number, patch_panel, connector) VALUE ('%d','%f','%f','%d','%d','%s','%s')"""%(int(DataInput['line_id']),float(DataInput['distance']),float(DataInput['gmap_distance']),int(DataInput['type_id']),int(DataInput['core']),str(DataInput['patch']),str(DataInput['connector']))
        cursor.execute(sql)
        db.commit()
        resp.body = json.dumps({"status": "success"})
        cursor.close()

class deletePath:
    cors = public_cors
    def on_get(self, req, resp):
        db = MySQLdb.connect(dbase,user,passw,dbname)
        cursor = db.cursor()
        data = []
        resp.status = falcon.HTTP_200
        DataInput = req.params
        sql = ("DELETE FROM polyline WHERE line_id = '"+ DataInput['line_id'] +"'")
        sql2 = ("DELETE FROM infoline WHERE connection_id = '"+ DataInput['line_id'] +"'")
        try:
            cursor.execute(sql)
            db.commit()
            cursor.execute(sql2)
            db.commit()
            resp.body = json.dumps({"status": "success"})
        except:
            db.rollback()
        cursor.close()

class addUser:
    cors = public_cors
    def on_post(self, req, resp):
        db = MySQLdb.connect(dbase,user,passw,dbname)
        cursor = db.cursor()
        data = []
        resp.status = falcon.HTTP_200
        DataInput = json.loads(req.stream.read())
        sql = """INSERT INTO user (username, password, firstname, lastname, tel, email, isadmin, reg_date) VALUE ('%s','%s','%s','%s','%d','%s','%d','%s')"""%(DataInput['username'],DataInput['password'],DataInput['firstname'],DataInput['lastname'],int(DataInput['tel']),DataInput['email'],int(DataInput['isAdmin']),str(datetime.datetime.now()+datetime.timedelta(hours=7)))
        cursor.execute(sql)
        db.commit()
        resp.body = json.dumps({"status": "success"})
        cursor.close()

class editUser:
    cors = public_cors
    def on_post(self, req, resp):
        db = MySQLdb.connect(dbase,user,passw,dbname)
        cursor = db.cursor()
        data = []
        resp.status = falcon.HTTP_200
        DataInput = json.loads(req.stream.read())
        sql = """UPDATE user SET firstname='%s', lastname='%s', tel='%d', email='%s', isadmin='%d' WHERE id = '%d';"""%(DataInput['firstname'],DataInput['lastname'],int(DataInput['tel']),DataInput['email'],int(DataInput['isAdmin']),int(DataInput['user_id']))
        cursor.execute(sql)
        db.commit()
        resp.body = json.dumps({"status": "success"})
        cursor.close()

class changePass:
    cors = public_cors
    def on_post(self, req, resp):
        db = MySQLdb.connect(dbase,user,passw,dbname)
        cursor = db.cursor()
        data = []
        resp.status = falcon.HTTP_200
        DataInput = json.loads(req.stream.read())
        sql = """UPDATE user SET password='%s' WHERE id = '%d';"""%(DataInput['password'],int(DataInput['user_id']))
        cursor.execute(sql)
        db.commit()
        resp.body = json.dumps({"status": "success"})
        cursor.close() 

class deleteUser:
    cors = public_cors
    def on_get(self, req, resp):
        db = MySQLdb.connect(dbase,user,passw,dbname)
        cursor = db.cursor()
        data = []
        resp.status = falcon.HTTP_200
        DataInput = req.params
        sql = ("DELETE FROM user WHERE id = '"+ DataInput['user_id'] +"'")
        try:
            cursor.execute(sql)
            db.commit()
            resp.body = json.dumps({"status": "success"})
        except:
            db.rollback()
        cursor.close()

class findLatLng:
    cors = public_cors
    def on_get(self, req, resp):
        db = MySQLdb.connect(dbase,user,passw,dbname)
        cursor = db.cursor()
        data = []
        resp.status = falcon.HTTP_200
        DataInput = req.params
        sql = ("SELECT d1.id, d1.name, d1.model, d2.lat, d2.lng, d2.ip ip_addr, d2.is_core, d1.uptime, d1.timestamp FROM device AS d1 INNER JOIN ip AS d2 ON d1.ip_addr=d2.id where name = '"+DataInput['A']+"' or name = '"+DataInput['B']+"';")
        cursor.execute(sql)
        req_data = cursor.fetchall()
        for x in req_data:
            if(x[7]!=0):
                time = str(datetime.timedelta(seconds=x[7]))
                temp = {"id":str(x[0]), "name":x[1],"position":{"lat":float(x[3]),"lng":float(x[4])}}
            else:
                time = str(datetime.timedelta(seconds=x[7]))
                temp = {"id":str(x[0]), "name":x[1],"position":{"lat":float(x[3]),"lng":float(x[4])}}
            data.append(temp)
        resp.body = json.dumps(data)
        cursor.close()

class getPathEdit:
    cors = public_cors
    def on_get(self, req, resp):
        db = MySQLdb.connect(dbase,user,passw,dbname)
        cursor = db.cursor()
        data = []
        resp.status = falcon.HTTP_200
        DataInput = req.params
        sql = ("SELECT * FROM polyline WHERE line_id = '"+DataInput['line_id']+"'")
        cursor.execute(sql)
        req_data = cursor.fetchall()
        for i in req_data:
            temp = {"id":i[0], "line_id":i[1], "seq":i[2], "lat":float(i[3]), "lng":float(i[4]), "colorline":i[5]}
            data.append(temp)
        resp.body = json.dumps(data)
        cursor.close()

class saveFlagPath:
    cors = public_cors
    def on_get(self, req, resp):
        client = MongoClient('mongodb://l3l3allza:123456@ds229549.mlab.com:29549/appharbor_j9h62tbg')
        db = client.appharbor_j9h62tbg
        col = db.saveFlagPath
        resp.status = falcon.HTTP_200
        col = db.saveFlagPath
        last_id = col.find().sort([
            ("_id", pymongo.DESCENDING)
        ]).limit(1)
        try:
            last_id = last_id[0]['_id']+1
        except:
            last_id = 0
        DataInput = req.params
        data = {"_id":last_id,"path":DataInput['path']}
        result = col.insert_one(data)
        resp.body = json.dumps(DataInput['path'])

class loadFlagPath:
    cors = public_cors
    def on_get(self, req, resp):
        client = MongoClient('mongodb://l3l3allza:123456@ds229549.mlab.com:29549/appharbor_j9h62tbg')
        db = client.appharbor_j9h62tbg
        col = db.saveFlagPath
        resp.status = falcon.HTTP_200
        col = db.saveFlagPath
        last_id = col.find().sort([
            ("_id", pymongo.DESCENDING)
        ]).limit(1)
        last_id = last_id[0]['_id']
        # DataInput = req.params
        # data = {"_id":last_id,"path":DataInput['path']}
        # result = col.insert_one(data)
        delet = col.remove({'_id':last_id})
        result = col.find().sort([("_id", pymongo.DESCENDING)]).limit(1)
        resp.body = json.dumps(result[0])

api.add_route('/authuser',authUser())
api.add_route('/addswitch',addSwitch())
api.add_route('/editswitch',editSwitch())
api.add_route('/deleteip',deleteIp())

api.add_route('/addpath',addPath())
api.add_route('/addinfoline',addInfoLine())
api.add_route('/deletepath',deletePath())

api.add_route('/adduser',addUser())
api.add_route('/edituser',editUser())
api.add_route('/changepass',changePass())
api.add_route('/deleteuser',deleteUser())

api.add_route('/findlatlng',findLatLng())
api.add_route('/getpathedit',getPathEdit())

api.add_route('/saveflagpath',saveFlagPath())
api.add_route('/loadflagpath',loadFlagPath())