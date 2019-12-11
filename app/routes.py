#从app模块中即从__init__.py中导入创建的app应用
from app import app
from flask import render_template
from flask import request
from app import init_db
import  ipdb
import pymongo
import configparser
import sys
import psycopg2
# read the attributes from the config
conf = configparser.ConfigParser()
conf.read("database.conf")
pos_dbname = conf.get('postgresql', 'db_name')
pos_host = conf.get('postgresql', 'db_host')
pos_port = conf.getint('postgresql', 'db_port')
pos_user = conf.get('postgresql', 'db_user')
pos_pwd = conf.get('postgresql', 'db_password')
mongo_dbname = conf.get('mongodb', 'db_name')
mongo_host = conf.get('mongodb', 'db_host')
mongo_port = conf.getint('mongodb', 'db_port')

#create tables
try:
    conn = psycopg2.connect(user=pos_user, password=pos_pwd, host=pos_host, port=pos_port,database=pos_dbname)
except:
    print('I am unable to connect the database')
    sys.exit(1)
cursor = conn.cursor()

#connect the mongodb

client = pymongo.MongoClient(host = mongo_host,port = mongo_port)
db = client[mongo_dbname]



#build the routers
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/wifiresult',methods=['GET','POST'])
def wifi_result():
    if request.method == 'POST':
        wifiType = request.values.get("wifiTypeSel")
        neighboorhood  =  request.values.get("neighboorhood")
        wifi_list = db["wifi"].find({'neighboorhood':neighboorhood,'wifiType':wifiType})
        count = db["wifi"].find({'neighboorhood':neighboorhood,'wifiType':wifiType}).count()
        return render_template('wifiresult.html',count = count,wifi_list = wifi_list)

@app.route('/wifineareresult',methods=['GET','POST'])
def wifinearE_result():
    if request.method == 'POST':
        id = request.values.get("id")
        entrance = db["entrances"].find_one({'objectID':id})
        e_lat = entrance["latitude"]
        e_lon = entrance["longitude"]
        count = db["wifi"].find({'latitude':{'$gt': e_lat-0.01,'$lt': e_lat+0.01},'longitude':{'$gt': e_lon-0.01,'$lt': e_lon+0.01}}).count()
        wifi_list  = db["wifi"].find({'latitude':{'$gt': e_lat-0.01,'$lt': e_lat+0.01},'longitude':{'$gt': e_lon-0.01,'$lt': e_lon+0.01}})
        return render_template('wifiresult.html',count = count,wifi_list = wifi_list)

@app.route('/restwithoutvio',methods=['GET','POST'])
def goodrestnl_result():
    if request.method == 'POST':
        id = request.values.get("id")
        name ="'%" + request.values.get("name") + "%'"

        query = 'SELECT restuarantName, cuisineType,address\
        From landmarks,restuarants\
        WHERE centerLogitude -restuarants.longitude <= 0.02 and centerLogitude -restuarants.longitude >= -0.02\
        and centerLatitude -restuarants.latitude <= 0.02 and centerLatitude -restuarants.latitude >= -0.02\
        and (landmarks.objectID = %s or landmarkName ilike %s )\
        and CAMIS not in (\
        Select CAMIS\
        From inspections\
        where extract(month from inspectiondate) =2019\
          );'
        cursor.execute(query %(id,name))
        records = cursor.fetchall()
        rest_list= []
        for record in records:
            new_rest = {}
            new_rest["name"] = record[0]
            new_rest["type"] = record[1]
            new_rest["address"] = record[2]
            rest_list.append(new_rest)
        query2 = 'SELECT count(CAMIS)\
        From landmarks,restuarants\
        WHERE centerLogitude -restuarants.longitude <= 0.02 and centerLogitude -restuarants.longitude >= -0.02\
        and centerLatitude -restuarants.latitude <= 0.02 and centerLatitude -restuarants.latitude >= -0.02\
        and (landmarks.objectID = %s or landmarkName ilike %s )\
        and CAMIS not in (\
        Select CAMIS\
        From inspections\
        where extract(month from inspectiondate) =2019\
          );'
        cursor.execute(query2 %(id,name))
        result = cursor.fetchall()
        count = result[0][0]
        return render_template('restaurant.html',count = count,rest_list = rest_list)

@app.route('/landmarknr')
def landmarknr_result():
    query = "select distinct landmarkname, sum(ct)/count(restuarants.CAMIS), count(restuarants.CAMIS)\
    from landmarks,\
    restuarants,\
    (Select count(CAMIS) as ct, CAMIS\
    From inspections\
    Group By CAMIS) ctCAMIS\
    WHERE centerLogitude -restuarants.longitude <= 0.02 and centerLogitude -restuarants.longitude >= -0.02\
    and centerLatitude -restuarants.latitude <= 0.02 and centerLatitude -restuarants.latitude >= -0.02\
    and ctCAMIS.CAMIS = restuarants.CAMIS\
    and restuarants.CAMIS in (\
    SELECT CAMIS\
    FROM grades\
    WHERE grade ='A'\
      )\
    Group by landmarkname\
    order by sum(ct)/count(restuarants.CAMIS), count(restuarants.CAMIS) DESC;"
    cursor.execute(query)
    records = cursor.fetchall()
    landmark_list = []
    for record in records:
        new_landmark = {}
        new_landmark["name"] = record[0]
        new_landmark["ratio"] = record[1]
        new_landmark["num"] = record[2]
        landmark_list.append(new_landmark)
    return render_template('landmarkresult.html',landmark_list = landmark_list)

@app.route('/restuarantSearchComplete',methods=['GET','POST'])
def restaurantSearch_results():
    if request.method == 'POST':    
        name ="'%" + request.values.get("name") + "%'"
        cuisineType = "'%" + request.values.get("type") + "%'"
        neigh = "'%" + request.values.get("neigh") + "%'"
        order = request.values.get("order")
        query = "select distinct CAMIS, restuarantName, longitude, latitude, cuisineType, neighborhood, street, zipcode, phone\
        FROM restuarants\
        WHERE restuarantName ilike %s AND\
        cuisineType ilike %s AND\
        neighborhood ilike %s\
        ORDER BY %s"

        cursor.execute(query %(name, cuisineType, neigh, order))
        records = cursor.fetchall()
        rest_list= []
        for record in records:
            new_rest = {}
            new_rest["CAMIS"] = record[0]
            new_rest["restaurantName"] = record[1]
            new_rest["longitude"] = record[2]
            new_rest["latitude"] = record[3]
            new_rest["cuisineType"] = record[4]
            new_rest["neighborhood"] = record[5]
            new_rest["street"] = record[6]
            new_rest["zipcode"] = record[7]
            new_rest["phone"] = record[8]
            rest_list.append(new_rest)
        return render_template('restaurantFull.html',rest_list = rest_list)

@app.route('/violationsForARestaurant',methods=['GET','POST'])
def restaurantVioSearch_results():
    if request.method == 'POST':    
        CAMIS_ID = request.values.get("name")
        expanded = request.values.get("expanded")
        query = "select CAMIS, restuarantName, longitude, latitude, cuisineType, neighborhood, street, zipcode, phone\
        FROM restuarants\
        WHERE CAMIS = '%s'"
        cursor.execute(query %(str(CAMIS_ID)))
        records = cursor.fetchall()
        rest_list= []
        for record in records:
            new_rest = {}
            new_rest["CAMIS"] = record[0]
            new_rest["restaurantName"] = record[1]
            new_rest["longitude"] = record[2]
            new_rest["latitude"] = record[3]
            new_rest["cuisineType"] = record[4]
            new_rest["neighborhood"] = record[5]
            new_rest["street"] = record[6]
            new_rest["zipcode"] = record[7]
            new_rest["phone"] = record[8]
            rest_list.append(new_rest)
        
        query2 = "select InspectionDate, ViolationCode\
            from inspections\
            where CAMIS = '%s'\
            Order By InspectionDate"
        cursor.execute(query2 %(CAMIS_ID))
        records2 = cursor.fetchall()
        violations = []
        if(expanded == "Yes"):
            for record in records2:
                new_rest = {}
                new_rest["InspectionDate"] = record[0]
                new_rest["ViolationCode"] = record[1]
                query3 = "select ViolationDescription\
                from violations\
                where violationID = '%s'"
                cursor.execute(query3 % (record[1]))
                descript = cursor.fetchall()
                new_rest["ViolationDescription"] = descript[0][0]
                violations.append(new_rest)
        else:
            for record in records2:
                new_rest = {}
                new_rest["InspectionDate"] = record[0]
                new_rest["ViolationCode"] = record[1]
                violations.append(new_rest)


        return render_template('violation.html', rest_list = rest_list, violationList = violations)

@app.route('/Neighboorhood_Features',methods=['GET','POST'])
def neighborhoodResults():
    if request.method == 'POST':    
        neigh = request.values.get("name")
        query1 = "select objectID, landmarkName, centerLogitude, centerLatitude, address\
        FROM landmarks\
        WHERE neighborhood ilike '%s'"
        cursor.execute(query1 %(str(neigh)))
        records1 = cursor.fetchall()
        for record in records1:
            new_rest = {}
            new_rest["ID"] = record[0]
            new_rest["name"] = record[1]
            new_rest["longitude"] = record[2]
            new_rest["latitude"] = record[3]
            new_rest["address"] = record[4]
            new_rest["type"] = "Landmark"          
            rest_list.append(new_rest)
        search = "/" + neigh + "/"   
        wifi_list = db["wifi"].find({'neighboorhood': search})
        for each in wifi_list:
            new_rest = {}
            new_rest["ID"] = each["wifiID"]
            new_rest["name"] = each["name"]
            new_rest["longitude"] = each["longitude"]
            new_rest["latitude"] = each["latitude"]
            new_rest["address"] = each["location"]
            new_rest["type"] = "Wifi"          
            rest_list.append(new_rest)
        query = "select CAMIS, restuarantName, longitude, latitude, street\
        FROM restuarants\
        WHERE neighborhood ilike '%s'"
        cursor.execute(query %(str(neigh)))
        records = cursor.fetchall()
        rest_list= []
        for record in records:
            new_rest = {}
            new_rest["ID"] = record[0]
            new_rest["name"] = record[1]
            new_rest["longitude"] = record[2]
            new_rest["latitude"] = record[3]
            new_rest["address"] = record[4]
            new_rest["type"] = "Restaurant"          
            rest_list.append(new_rest)
        return render_template('featuresNeigh.html', rest_list = rest_list)
