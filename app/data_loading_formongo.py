import psycopg2
from sodapy import Socrata
import pandas as pd
import pymongo
import csv
import regex as re
import ipdb

def calCenter(s):
    number_list = re.findall(r'\d+.\d+',s)
    odd_sum = 0
    even_sum = 0
    for i in range(len(number_list)):
        if i %2== 0:
            even_sum += float(number_list[i])
        else:
            odd_sum += float(number_list[i])

    long = even_sum/len(number_list)*2
    lat = odd_sum/len(number_list)*2

    return [lat,long]


#connect the mongodb
client = pymongo.MongoClient('127.0.0.1', 27017)
# create database
db = client['final_project']
# get the number of collections
collections = db.list_collection_names()
if len(collections) != 0:
    for col in collections:
        del_col = db[col]
        del_col.drop()
#create the collections landmark
cur_col = db["landmarks"]
csv.field_size_limit(100000000)
# read data from csv
with  open("data/landmark.csv", "r") as f:
    reader = csv.reader(f, quoting=csv.QUOTE_MINIMAL)
    landmark_list  = []

    for landmark in reader:

        if reader.line_num == 1:
            continue
        new_landmark = {}
        new_landmark["objectID"] = landmark[0]
        new_landmark["address"] =  landmark[5]
        new_landmark["landmarkName"] = landmark[7]
        new_landmark["centerLatitude"],new_landmark["centerLongitude"] = calCenter(landmark[1])
        new_landmark["additionalInfoURL"] = landmark[-1]
        landmark_list.append(new_landmark)
# insert data into database
cur_col.insert_many(landmark_list)

#create the collections entrances
cur_col = db["entrances"]

# read data from csv
with  open("data/subway.csv", "r") as f:
    reader = csv.reader(f, quoting=csv.QUOTE_MINIMAL)
    entrance_list  = []
    for entrance in reader:

        if reader.line_num == 1:
            continue
        new_entrance = {}
        new_entrance["objectID"] = entrance[0]
        new_entrance["name"] = entrance[2]
        loc_data = re.findall(r'\d+.\d+',entrance[3])
        new_entrance["longitude"], new_entrance["latitude"] = float(loc_data[0]),float(loc_data[1])
        new_entrance["line"] = entrance[-1].split('-')



        entrance_list.append(new_entrance)
# insert data into database
cur_col.insert_many(entrance_list)


#create the collections wifi
cur_col = db["wifi"]

# read data from csv
with  open("data/wifi.csv", "r",encoding="utf-8") as f:
    reader = csv.reader(f, quoting=csv.QUOTE_MINIMAL)
    wifi_list  = []
    for wifi in reader:
        if reader.line_num == 1:
            continue
        new_wifi = {}
        new_wifi["wifiID"] = wifi[2]
        loc_data = re.findall(r'\d+.\d+',wifi[1])
        new_wifi["longitude"], new_wifi["latitude"] = float(loc_data[0]),float(loc_data[1])
        new_wifi["wifiType"] = wifi[3]
        new_wifi["provider"] = wifi[4]
        new_wifi["name"] = wifi[5]
        new_wifi["location"] = wifi[6]
        new_wifi["remarks"] = wifi[12]
        new_wifi["neighboorhood"] = wifi[18]
        new_wifi["ssid"] = wifi[14]
        new_wifi["activatedDate"] = wifi[16]
        new_wifi["NTACODE"] = wifi[19]
        new_wifi["NTANAME"] = wifi[20]
        wifi_list.append(new_wifi)
# insert data into database
cur_col.insert_many(wifi_list)
