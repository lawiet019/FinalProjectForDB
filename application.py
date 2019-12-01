#!/usr/bin/env python
from flask import Flask
from flask_restful import Resource, Api
import pymongo
import psycopg2
import pandas as pd

import dataloading, data_loading_formongo

try:
    conn = psycopg2.connect("dbname = 'itws6960_project' user = 'postgres' host = 'localhost'")
except psycopg2.DatabaseError:
    print('I am unable to connect the database')
    sys.exit(1)

cursor = conn.cursor()

from pymongo import MongoClient
client = MongoClient()



app = Flask(__name__)
api = Api(app)

