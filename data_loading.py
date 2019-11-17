#!/usr/bin/env python
"""

"""
import psycopg2
import pandas as pd
from sodapy import Socrata

conn = psycopg2.connect("host=localhost dbname=itws6960_project user=postgres")
client = Socrata("data.cityofnewyork.us", None)


RESTAURANT_DATASET_IDENTIFIER = "43nn-pn8j"
WIFI_DATASET_IDENTIFIER = "yjub-udmw"
SUBWAY_DATASET_IDENTIFIER = "i9wp-a4ja"
LANDMARK_DATASET_IDENTIFIER = "7mgd-s57w"
# IMPORT CSVs for SUBWAY DATASET AND LANDMARK DATASET INSTEAD, BECUASE NEITHER IDENIFIER WANTS TO WORK 

results = client.get(RESTAURANT_DATASET_IDENTIFIER, limit = 400000)

results_df = pd.DataFrame.from_records(results)

print(results_df)


if __name__ == '__main__':    #code to execute if called from command-line
    pass    #do nothing - code deleted