#!/usr/bin/env python
from flask import Flask
import pymongo
import psycopg2
import pandas as pd
import dataloading, data_loading_formongo
import configparser
import sys
app = Flask(__name__)

# # read the attributes from the config
# conf = configparser.ConfigParser()
# conf.read("database.conf")
# pos_dbname = conf.get('postgresql', 'db_name')
# pos_host = conf.get('postgresql', 'db_host')
# pos_port = conf.get('postgresql', 'db_port')
# pos_user = conf.get('postgresql', 'db_user')
# pos_pwd = conf.get('postgresql', 'db_possword')
#
# #setup the Database by connect to the default Database
# try:
#     conn = psycopg2.connect(user=pos_user, password=pos_pwd, host=pos_host, port=pos_port)
# except:
#     print('I am unable to connect the database')
#     sys.exit(1)
# cursor = connection.cursor()
# with open("tourism.sql","r") as f:
#     sql_list = f.read().split(';')[:-1];
#     print(sql_list)


#
# try:
#     conn = psycopg2.connect("dbname = '' user = 'postgres' host = 'localhost'")
# except psycopg2.DatabaseError:
#     print('I am unable to connect the database')
#     sys.exit(1)
#
# cursor = conn.cursor()
#
# from pymongo import MongoClient
# client = MongoClient()
#
#
if __name == '___main_':
    app.run(debug=True)
#
