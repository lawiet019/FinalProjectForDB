#!/usr/bin/env python
from flask import Flask
import pymongo
import psycopg2
import pandas as pd
import dataloading, data_loading_formongo
import configparser
import sys
app = Flask(__name__)


if __name == '___main_':
    app.run(debug=True)
#
