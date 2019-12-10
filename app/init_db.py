import sys
import psycopg2
import configparser

# read the attributes from the config
conf = configparser.ConfigParser()
conf.read("database.conf")

pos_dbname = conf.get('postgresql', 'db_name')
pos_host = conf.get('postgresql', 'db_host')
pos_port = conf.getint('postgresql', 'db_port')
pos_user = conf.get('postgresql', 'db_user')
pos_pwd = conf.get('postgresql', 'db_password')

#create tables
try:
    conn = psycopg2.connect(user=pos_user, password=pos_pwd, host=pos_host, port=pos_port,database=pos_dbname)
except:
    print('I am unable to connect the database')
    sys.exit(1)
with conn.cursor() as cursor:
    with open('SQL/create-tables.sql', 'r') as restaurant_data:
        setup_queries = restaurant_data.read()
        cursor.execute(setup_queries)
    conn.commit()
from app import data_loading_formongo
from app import dataloading
