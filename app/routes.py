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
P_cursor = conn.cursor()

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
        city  =  request.values.get("city")
        wifi_list = db["wifi"].find({'city':city,'wifiType':wifiType})
        count = db["wifi"].find({'city':city,'wifiType':wifiType}).count()
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
