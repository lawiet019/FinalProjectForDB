import psycopg2
from sodapy import Socrata
import pandas as pd
import sys
import re
RESTAURANT_DATASET_IDENTIFIER = "43nn-pn8j"
'''
    table                 done
    inspections            x
    grades                 x
    restuarants            x
    violations             x
    landmarks              x

'''

client = Socrata("data.cityofnewyork.us", None)
results = client.get(RESTAURANT_DATASET_IDENTIFIER)

full_restuarant_df = pd.DataFrame.from_records(results)

try:
    conn = psycopg2.connect("dbname = 'itws6960_project' user = 'postgres' password='abC123456' host = 'localhost'")
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
    inspections_df['score'][i] = str(inspections_df['score'])
    if inspections_df['score'][i] == 'nan':
        inspections_df['score'][i] = None
    if inspections_df['score'][i] != None:
        try:
            inspections_df['score'][i] =  int(inspections_df['score'][i])
        except:
            inspections_df['score'][i] = None
    query =  """INSERT INTO inspections VALUES (%s, %s, %s, %s)"""
    record = (inspections_df['CAMIS'][i],
            inspections_df['inspectionDate'][i].split('T')[0],
            inspections_df['violationCodes'][i],
            inspections_df['score'][i])
    cursor.execute(query, record)
    conn.commit()




data =  {'CAMIS': list(full_restuarant_df['camis']),
        'gradeDate': list(full_restuarant_df['grade_date']),
        'grade': list(full_restuarant_df['grade'])
        }
grades_df = pd.DataFrame(data)

for i in range(0, len(grades_df)):
    grades_df['gradeDate'][i] = str(grades_df['gradeDate'][i])
    grades_df['grade'][i] = str(grades_df['grade'][i])

    if grades_df['gradeDate'][i] == 'nan':
        grades_df['gradeDate'][i] = None
    if grades_df['grade'][i] == 'nan':
        grades_df['grade'][i] = None

    query =  """INSERT INTO grades (CAMIS, GradeDate, grade) VALUES (%s, %s, %s)"""
    record = (grades_df['CAMIS'][i], grades_df['gradeDate'][i], grades_df['grade'][i])
    cursor.execute(query, record)
    conn.commit()


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

for i in range(0, len(restuarants_df)):
    restuarants_df['phone'][i] = str(restuarants_df['phone'][i])
    if restuarants_df['phone'][i] == 'nan':
         restuarants_df['phone'][i] = None
    restuarants_df['zipcode'][i] = str(restuarants_df['zipcode'][i])
    if restuarants_df['zipcode'][i] == 'nan':
         restuarants_df['zipcode'][i] = None
    if restuarants_df['zipcode'][i] !=  None:
        restuarants_df['zipcode'][i] = int(restuarants_df['zipcode'][i])
    restuarants_df['restuarantName'][i] = str(restuarants_df['restuarantName'][i])
    restuarants_df['restuarantName'][i] =restuarants_df['restuarantName'][i].replace("'","")
    restuarants_df['longitude'][i] = float(restuarants_df['longitude'][i])
    restuarants_df['longitude'][i] = abs(restuarants_df['longitude'][i])
    cursor.execute( "INSERT INTO restuarants (CAMIS,longitude, latitude, restuarantName,cuisineType, street, zipcode, phone)  VALUES ('%s', '%s', '%s', '%s', '%s','%s', '%s', '%s')" %
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
    conn.commit()


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

for i in range(0, len(violations_df)):

    violations_df['violationDescription'][i] = str(violations_df['violationDescription'][i])
    violations_df['violationDescription'][i] = violations_df['violationDescription'][i].replace("'","")


    if violations_df['violationDescription'][i] == 'nan':
        violations_df['violationDescription'][i] = None
    cursor.execute( "INSERT INTO violations VALUES ('%s', '%s')" %
                    (violations_df['violationCode'][i],
                    violations_df['violationDescription'][i]
                    )
        )
    conn.commit()


landmarks_df = pd.read_csv("data/landmark.csv")


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

for i in range(0, len(landmarks_df)):
    landmarks_df['LPC_NAME'][i] =landmarks_df['LPC_NAME'][i].replace("'","")
    landmarks_df['URL_REPORT'][i] =landmarks_df['URL_REPORT'][i].replace("'","")
    landmarks_df['Address'][i] = str(landmarks_df['Address'][i])
    landmarks_df['Address'][i] =landmarks_df['Address'][i].replace("'","")
    centerLatitude, centerLogitude = calCenter(landmarks_df['the_geom'][i])
    neighboorhood = landmarks_df['Borough'][i]
    print(neighboorhood)
    cursor.execute( "INSERT INTO landmarks (objectID, landmarkName,centerLogitude ,centerLatitude , neighborhood, address, additionalInfoURL) VALUES ('%s', '%s', '%s', '%s', '%s',  '%s', '%s')" %
                    (landmarks_df['OBJECTID'][i],
                    landmarks_df['LPC_NAME'][i],
                    centerLogitude,
                    centerLatitude,
                    neighboorhood,
                    landmarks_df['Address'][i],
                    landmarks_df['URL_REPORT'][i]
                    )
        )
    conn.commit()
