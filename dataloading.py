import psycopg2
from sodapy import Socrata
import pandas as pd

RESTAURANT_DATASET_IDENTIFIER = "43nn-pn8j"
'''
    table                 done
    inspections               
    grades                  
    restuarants             
    violations              
'''

client = Socrata("data.cityofnewyork.us", None)
results = client.get(RESTAURANT_DATASET_IDENTIFIER, limit = 10)
full_restuarant_df = pd.DataFrame.from_records(results)

try:
    conn = psycopg2.connect("dbname = 'itws6960_project' user = 'postgres' host = 'localhost'")
except psycopg2.DatabaseError:
    print('I am unable to connect the database')
    sys.exit(1)

cursor = conn.cursor()

data =  {'CAMIS': list(full_restuarant_df['camis']), 
        'inspectionDate': list(full_restuarant_df['inspection_date']),
        'violationCodes': list(full_restuarant_df['violation_code']),
        'score': list(full_restuarant_df['score'])
        }
inspections_df = pd.DataFrame(data)

for i in range(0, len(inspections_df)):
    cursor.execute( "INSERT INTO inspections VALUES (%s, %s, %s, %s)" % 
                    (inspections_df['CAMIS'][i], 
                    inspections_df['inspectionDate'][i].split('T')[0],
                    str(inspections_df['violationCodes'][i]),
                    str(inspections_df['score'][i])
                    )
        )

conn.commit()

data =  {'CAMIS': list(full_restuarant_df['camis']), 
        'gradeDate': list(full_restuarant_df['grade_date']),
        'grade': list(full_restuarant_df['grade'])
        }
grades_df = pd.DataFrame(data)
'''
for i in range(0, len(grades_df)):
    cursor.execute( "INSERT INTO grades VALUES (%s, %s, %s)" % 
                    (grades_df['CAMIS'][i], 
                    grades_df['gradeDate'][i],
                    grades_df['grade'][i]
                    )
        )
''' 

data =  {'CAMIS': list(full_restuarant_df['camis']),
        'longitude': list(full_restuarant_df['longitude']),
        'latitude': list(full_restuarant_df['latitude']),
        'restuarantName': list(full_restuarant_df['dba']),
        'cuisineDescription': list(full_restuarant_df['cuisine_description']),
        'street': list(full_restuarant_df['street']),
        'zipcode': list(full_restuarant_df['zipcode']),
        'phone': list(full_restuarant_df['phone'])
        }
restuarants_df = pd.DataFrame(data)
'''
for i in range(0, len(restuarants_df)):
    cursor.execute( "INSERT INTO restuarants VALUES (%s, %s, %s,%s, %s, %s,%s, %s)" % 
                    (restuarants_df['CAMIS'][i], 
                    restuarants_df['longitude'][i],
                    restuarants_df['latitude'][i],
                    restuarants_df['restuarantName'][i],
                    restuarants_df['cuisineDescription'][i],
                    restuarants_df['street'][i],
                    restuarants_df['zipcode'][i],
                    restuarants_df['phone'][i]
                    )
        )
''' 
data =  {'violationCode': full_restuarant_df['violation_code'],
        'violationDescription': full_restuarant_df['violation_description']
        }
violations_df = pd.DataFrame(data)


violations_dict = {}
for i in range(0, len(violations_df)):
    code = violations_df['violationCode'][i]
    if code not in violations_dict:
        violations_dict[code] = violations_df['violationDescription'][i]

violations_df = pd.DataFrame(list(violations_dict.items()), columns=list(violations_df.columns) )
'''
for i in range(0, len(violations_df)):
    cursor.execute( "INSERT INTO grades VALUES (%s, %s)" % 
                    (violations_df['violationCode'][i], 
                    violations_df['violationDescription'][i]
                    )
        )
''' 
conn.commit() 
# violation_code
# violation_description