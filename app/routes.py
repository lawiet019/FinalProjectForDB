#从app模块中即从__init__.py中导入创建的app应用
from app import app

from app import init_db

import pymongo
import configparser
import sys
import psycopg2
# read the attributes from the config
conf = configparser.ConfigParser()
conf.read("app/database.conf")
pos_dbname = conf.get('postgresql', 'db_name')
pos_host = conf.get('postgresql', 'db_host')
pos_port = conf.getInt('postgresql', 'db_port')
pos_user = conf.get('postgresql', 'db_user')
pos_pwd = conf.get('postgresql', 'db_password')
mongo_dbname = conf.get('mongodb', 'db_name')
mongo_host = conf.get('mongodb', 'db_host')
mongo_port = conf.getInt('mongodb', 'db_port')
mongo_user = conf.get('mongodb', 'db_user')
mongo_pwd = conf.get('mongodb', 'db_password')
#create tables
try:
    conn = psycopg2.connect(user=pos_user, password=pos_pwd, host=pos_host, port=pos_port,database=pos_dbname)
except:
    print('I am unable to connect the database')
    sys.exit(1)
P_cursor = conn.cursor()

#connect the mongodb
client = pymongo.MongoClient(mongo_host, mongo_port)
db = client[mongo_dbname]
db.authenticate(mongo_user, mongo_pwd)


# #build the routers
# @app.route('/')
# @app.route('/index')
# def index():
#     return "Hello,World!"
